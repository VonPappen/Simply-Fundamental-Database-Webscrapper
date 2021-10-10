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
from models import Security, Base
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URI)
session = sessionmaker(bind=engine)

s = session()

N = Nasdaq()
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

tickers = N.earnings_release_tickers(date=datetime.date.today())

if tickers is not None:


    df_earnings = pd.DataFrame()
    df_earnings['date'] = [datetime.date.today()] * len(tickers)
    df_earnings['ticker'] = tickers

    querry = s.query(Security.ticker, Security.id).all()
    security_map = {querry[i][0]: querry[i][1] for i, v in zip(range(len(querry)), range(len(querry)))}

    df_earnings['security_id'] = df_earnings['ticker'].map(security_map)


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
            period_list_on_db = []

            for stmnt in statements:
                for t_format in time_format:

                    r = s.query(Base.metadata.tables[f'{stmnt}_{t_format}'].columns['date']).where(
                        Base.metadata.tables[f'{stmnt}_{t_format}'].columns['ticker'] == str(ticker)
                    ).all()
                    r.sort(reverse=True)
                    r =  str(r[0][0])
                    period_list_on_db.append(r)

            r = max(period_list_on_db)

            return convert_to_ending_period_format(r)
        
        except:
        
            return None

    data = N.earnings_release(datetime.date.today())
    df_earnings['last_period_N'] = data['fiscalQuarterEnding'].map(convert_date_N)
    df_earnings['last_period_DB'] = df_earnings['ticker'].map(last_period_db)
    df_earnings['last_period_M'] = df_earnings['ticker'].map(M.latest_ending_period_available)

    print(df_earnings)
    try:
        df_earnings.to_sql(con=engine, name="earnings_release", index=False, if_exists="append")
    except:
        print("earnings table is already up to date")

else:
    print('No data to collect today')
    pass

s.close_all()