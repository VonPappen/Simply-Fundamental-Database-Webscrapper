#!/usr/bin/env python3
# Don't forget the SHEBANG

# TODO: FIND OUT WHY THE SCRIPT STOPS HALFWAY THROUGH
import sys, os
import datetime
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(
                __file__
            )
        )
    )
)

from scrapping_sources.Finviz import Finviz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Security
from config import DATABASE_URI
import time

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()
finviz_scrapper = Finviz()

q = s.query(Security).all()
tickers_in_database = [i.ticker for i in q]

start = time.perf_counter()
finviz_table = None

# Retry for 3 hours.
while finviz_table is None and (time.perf_counter() - start) < 60*60*3 :
    try:
        finviz_table = finviz_scrapper.generate_security_table()
    except:
        # FIND A WAY TO CATCH THIS ERROR
        load = pd.DataFrame(
            [
                {
                    "date":str(datetime.datetime.today()),
                    "log":"Unable to fetch data from finviz",
                    "status":"FAILURE",
                    "added": ""
                }
            ]
        )
        load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")
        pass

if finviz_table is not None:
    tickers_in_finviz = [i for i in finviz_table.ticker]
    list_of_tickers_to_add = list(set(tickers_in_finviz) - set(tickers_in_database))
    print(f"Tickers to add: {list_of_tickers_to_add}")

    if len(list_of_tickers_to_add) == 0:
        load = pd.DataFrame(
            [
                {
                    "date":str(datetime.datetime.today()),
                    "log":"up to date",
                    "status":"SUCCESS",
                    "added": ""
                }
            ]
        )
        load.to_sql(
            con=engine,
            name="securities_table_log",
            index=False,
            if_exists="append"
        )
    else:
        update_table = finviz_table[finviz_table.ticker.isin(list_of_tickers_to_add)]
        update_table.to_sql(con= engine, if_exists='append', index=False, name= 'securities_table')
        # Update securities_table_log
        for symbol in list_of_tickers_to_add:
            load = pd.DataFrame(
                [
                    {
                        "date":str(datetime.datetime.today()),
                        "log":"updated",
                        "status":"SUCCESS",
                        "added": str(symbol)
                    }
                ]
            )
            load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")
else:
    pass

s.close_all()