#!/usr/bin/env python3
import sys, os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(
                __file__
            )
        )
    )
)

from scrapping_sources.Macrotrend import Macrotrend
from scrapping_sources.Nasdaq import Nasdaq

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Security, Base
from config import DATABASE_URI

import pandas as pd
import datetime

engine = create_engine(DATABASE_URI)
session = sessionmaker(bind=engine)
s = session()
# my_db = Database()
Nasdaq_scrapper = Nasdaq()
Macrotrend_scrapper = Macrotrend()

# r = s.query(Security.ticker).all()

# security_map = [i[0] for i in r]
# print(security_map)
#####
querry = s.query(Security.ticker, Security.id).all()
security_map = {querry[i][0]: querry[i][1] for i, v in zip(range(len(querry)), range(len(querry)))}

def check_if_security_exists(ticker_):
    try:
        s.query(Security.ticker).filter_by(ticker=f"{ticker_}").first()[0]
        return True
    except:
        return False

def fetch_all_statements(ticker_, statement, time_format):
    result = s.query(
        Base.metadata.tables[f"{statement.replace('-','_')}_{time_format}"]
        ).filter_by(ticker=f'{ticker_}').all()
    return result


statements   = [
    'income-statement',
    'balance-sheet',
    'cash-flow-statement',
    'financial-ratios'
            ]

time_formats = [
    'quarterly', 
    'annual'
    ]
day_variable = 7

df = Nasdaq_scrapper.earnings_release(str(datetime.date.today() - datetime.timedelta(days = day_variable)))



try:
    InDB = [i for i in df['symbol'].values if check_if_security_exists(i)]
    latest_ending_period_nasdaq = [Nasdaq_scrapper.latest_ending_period_available(i, datetime.date.today() - datetime.timedelta(days= day_variable)) for i in InDB]
    
except:
    latest_ending_period_nasdaq = []
    InDB = []

if len(InDB)==0:
    load = pd.DataFrame(
        [
            {
                "date"      : f"{datetime.datetime.today()}",
                "log"       : "Up To Date",
                "status"    : "SUCCESS",
                "added"     : "No Data to update",
                "days_after_release" : 14
            }
        ]
    )
else:
    pass


no_data_on_trend = []
success = []
to_update = []

for tick in InDB:
    for time_format in time_formats:
        for stmnt in statements:
            print(tick, stmnt, time_format)
            latest = Macrotrend_scrapper.arrange_data(tick, stmnt, time_format)
            in_database = pd.DataFrame(fetch_all_statements(tick, stmnt, time_format))

            try:
                in_database.columns = ['id','date','statement','ticker', 'security_id', 'line_item', 'amount']
                in_database['security_id'] = in_database.ticker.map(security_map)
                in_database = Macrotrend_scrapper.move_column(in_database, 'security_id', 3)
                latest['security_id'] = latest.ticker.map(security_map)

                convert_dict = {'date': str,
                                'statement': str,
                                'ticker': str,
                                'security_id': int,
                                'line_item': str,
                                'amount': float
                }
                in_database = in_database.astype(convert_dict)
                latest = latest.astype(convert_dict)
                
            except:
                pass

            if isinstance(in_database, pd.DataFrame) and isinstance(latest, pd.DataFrame):

                if latest.shape[0] == in_database.shape[0]:

                    pass
                
                elif in_database.empty:

                    latest['date'] = pd.to_datetime(latest.date)
                    update = latest
                    update['amount'] = pd.to_numeric(update['amount'])
                    update['security_id'] = update.ticker.map(security_map)

                    update.to_sql(con = engine, name=f"{stmnt.replace('-','_')}_{time_format}", if_exists='append', index=False)

                    success.append((tick, stmnt, time_format))
                    

                else:
                    print("IN DATABASE", in_database)
                    in_database['date'] = pd.to_datetime(in_database['date'])
                    indb_date_set = set(in_database.date.values)
                    latest['date'] = pd.to_datetime(latest.date)
                    update_date_set = set(latest.date.values)
                    update = latest[latest.date.isin(list(update_date_set - indb_date_set))]
                    to_update.append((tick, stmnt, time_format))
                    update['amount'] = pd.to_numeric(update['amount'])
                    update['security_id'] = update.ticker.map(security_map)
                    # print(update)
                    update.to_sql(con = engine, name=f"{stmnt.replace('-','_')}_{time_format}", if_exists='append', index=False)

                    success.append((tick, stmnt, time_format))
                    
            else:

                no_data_on_trend.append(tick)

                pass

if len(success) >= 1 :

    load = pd.DataFrame(
        [
            {
                "date"      : f"{datetime.datetime.today()}",
                "log"       : "updating",
                "status"    : "SUCCESS",
                "added"     : f"{success}",
                "days_after_release" : 7
            }
        ]
    )
else:

    load = pd.DataFrame(
        [
            {
                "date"      : f"{datetime.datetime.today()}",
                "log"       : "Up To Date",
                "status"    : "SUCCESS",
                "added"     : "No Data to update",
                "days_after_release" : 7
            }
        ]
    )
if len(set(to_update)-set(success)) > 0:
    failure = pd.DataFrame(
            [
                {
                    "date"      : f"{datetime.datetime.today()}",
                    "log"       : "updating",
                    "status"    : "FAILURE",
                    "added"     : f"Failed to add: {set(to_update)-set(success)}",
                    "days_after_release" : 7
                }
            ]
        )
    failure.to_sql(con = engine, name="statements_table_log", if_exists='append', index=False)

load.to_sql(con = engine, name="statements_table_log", if_exists='append', index=False)
print(f"To update: {to_update}")
print(f"Successfully updated: {success}")
print(f"SET(TO UPDATE - SUCCESS) = {set(to_update) - set(success)}")
print('Done.')
s.close_all()