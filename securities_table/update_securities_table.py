#!/usr/bin/env python3
# Don't forget the SHEBANG

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

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()
finviz_scrapper = Finviz()


q = s.query(Security).all()
tickers_in_database = [i.ticker for i in q]
print(tickers_in_database)


finviz_table = finviz_scrapper.generate_security_table()
tickers_in_finviz = [i for i in finviz_table.ticker]
list_of_tickers_to_add = list(set(tickers_in_finviz) - set(tickers_in_database))

if len(list_of_tickers_to_add) == 0:
    load = pd.DataFrame(
        [
            {
                "date":str(datetime.date.today()),
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

elif len(list_of_tickers_to_add) > 1000:

    update_table = finviz_table[finviz_table.ticker.isin(list_of_tickers_to_add)]
    update_table.to_sql(con= engine, if_exists='append', index=False, name= 'securities_table')
    # Update securities_table_log
    load = pd.DataFrame(
        [
            {
                "date":str(datetime.date.today()),
                "log":"updated",
                "status":"INITIALIZED",
                "added": f"added {str(len(list_of_tickers_to_add))} securities on initialization"
            }
        ]
    )
    load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")

else:
    try:
        update_table = finviz_table[finviz_table.ticker.isin(list_of_tickers_to_add)]
        update_table.to_sql(con= engine, if_exists='append', index=False, name= 'securities_table')
        # Update securities_table_log
        load = pd.DataFrame(
            [
                {
                    "date":str(datetime.date.today()),
                    "log":"updated",
                    "status":"SUCCESS",
                    "added": str(list_of_tickers_to_add)
                }
            ]
        )
        load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")
    except:
        #TODO: add an email alert if possible
        load = pd.DataFrame(
            [
                {
                    "date":str(datetime.date.today()),
                    "log":"",
                    "status":"FAILURE",
                    "added": ""
                }
            ]
        )
        load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")

s.close_all()