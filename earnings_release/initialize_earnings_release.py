# COLLECT DATA 30 DAYS PRIOR IN ORDER TO HAVE THE EARNINGS TABLE READY TO UPDATE EVERYTHING

import os, sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(
                __file__
            )
        )
    )
)

import datetime
import pandas as pd
from scrapping_sources.Nasdaq import Nasdaq
from scrapping_sources.Macrotrend import Macrotrend
from models import Earnings_release, Security, Base
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URI)
session = sessionmaker(bind=engine)

s = session()

N = Nasdaq()
print(N.earnings_release_tickers("2021-08-27"))
M = Macrotrend()

statements = [
'income_statement',
'balance_sheet',
'cash_flow_statement',
'financial_ratios'
]
time_format = [
    'annual',
    'quarterly'
]

day_gap = [datetime.date.today() - datetime.timedelta(days= i) for i in range(0,30)]
#list of date dates 0 days looking back period

def convert_date_N(date):
    """Converts the data from Nasdaq scrapper to same format"""
    return datetime.datetime.strptime(str(date), '%b/%Y').strftime("%Y-%m")

def convert_to_ending_period_format(date):
    """Converts the data from Database scrapper to same format"""
    result = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime("%Y-%m")
    return result

def last_period_db(ticker):
    """Returns the the latest date available for statements in Database """
    try:
        r = s.query(Base.metadata.tables['income_statement_quarterly'].columns['date']).where(
            Base.metadata.tables['income_statement_quarterly'].columns['ticker'] == str(ticker)
        ).all()
        r.sort(reverse=True)
        r =  str(r[0][0])
        return convert_to_ending_period_format(r)
    except:
        return None


for date in day_gap:
    print(str(date))
    try:
        tickers = N.earnings_release_tickers(str(date))
        print(tickers)
    except:
        tickers = None
    if tickers is None:
        pass
    else:
        df_earnings = pd.DataFrame()
        df_earnings['date'] = [datetime.date.today()] * len(tickers)
        df_earnings['ticker'] = tickers
        df_earnings['release_date'] = date

        querry = s.query(Security.ticker, Security.id).all()
        security_map = {querry[i][0]: querry[i][1] for i, v in zip(range(len(querry)), range(len(querry)))}

        df_earnings['security_id'] = df_earnings['ticker'].map(security_map)

        # def is_in_database(ticker):
        #     """Returns True if ticker is in database"""
        #     query = s.query(Base.metadata.tables['securities_table'].columns['ticker']).all()
        #     if ticker in [i[0] for i in query]:
        #         return True
        #     else:
        #         return False

        # def has_f_data_in_db(ticker):
        #     data_boolean_list = []
        #     for stmnt in statements:
        #         for t_format in time_format:
        #             q = s.query(Base.metadata.tables[f'{stmnt}_{t_format}']).where(
        #                 Base.metadata.tables[f'{stmnt}_{t_format}'].columns['ticker'] ==str(ticker)).all()
        #             if len(q) == 0:
        #                 data_boolean_list.append(False)
        #             else:
        #                 data_boolean_list.append(True)
        #     return any(data_boolean_list)

        # def has_data_on_trend(ticker):
        #     _ = []
        #     for stmnt in statements:
        #         for t_format in time_format:
        #             r = M.arrange_data(ticker=ticker, statement= stmnt.replace('_', '-'), time_format=t_format)
        #             if r is not None:
        #                 _.append(True)
        #     return any(_)

        # df_earnings['in_db'] = df_earnings['ticker'].map(is_in_database)
        # df_earnings['in_db_f_data'] = df_earnings['ticker'].map(has_f_data_in_db)
        # df_earnings['trend_f_data'] = df_earnings['ticker'].map(has_data_on_trend)

        data = N.earnings_release(date)
        df_earnings['last_period_N'] = data['fiscalQuarterEnding'].map(convert_date_N)
        df_earnings['last_period_DB'] = df_earnings['ticker'].map(last_period_db)
        df_earnings['last_period_M'] = df_earnings['ticker'].map(M.latest_ending_period_available)

        # print(df_earnings)
        try:
            df_earnings.to_sql(con=engine, name="earnings_release", index=False, if_exists="append")
        except:
            print("earnings table is already up to date")

    # except:

    #     load = pd.DataFrame(
    #         [
    #             {
    #                 "date"          : str(datetime.date.today()),
    #                 "ticker"        : None,
    #                 "release_date"  : date,
    #                 # "statement"     : None,
    #                 # "time_format"   : None,
    #                 # "status"        : "No data",
    #                 "last_period_M" : None,
    #                 "last_period_DB": None,
    #                 "last_period_N" : None
    #             }
    #         ]
    #     )
    #     load.to_sql(con=engine, name="earnings_release", if_exists="append", index=False)

s.close_all()