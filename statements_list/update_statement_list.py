import sys, os

from sqlalchemy.sql.expression import table

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(
                __file__
            )
        )
    )
)

import pandas as pd
from scrapping_sources.Macrotrend import Macrotrend
from models import Security, Earnings_release
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import concurrent.futures
from itertools import repeat

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

s = Session()
r = s.query(Security.ticker, Security.id).all()
sec_id_map = {i[0]:i[1] for i in r}
tickers = s.query(Security.ticker).all()
tickers_list = [i[0] for i in tickers]
print(tickers_list)
M = Macrotrend()

statements = [
    'income-statement',
    'balance-sheet',
    'cash-flow-statement',
    'financial-ratios'
]
time_format = [
    'annual',
    'quarterly'
]



def generate_statement_list(ticker, statement, time_format):

    df = M.arrange_data(ticker, statement, time_format)
    if df is not None:
        df = df[['date','ticker', 'statement', 'security_id']].drop_duplicates()
        df["security_id"] = df["ticker"].map(sec_id_map)
        # Getting there, but what's next?...
        # 1 - Create a statement_id
        # 
        return df

def generate_statement_list_multi(ticker_list, statement, time_format):

    table = []

    def create_table(ticker, statement, time_format):

        """Creates a table from ticker"""
        df = generate_statement_list(ticker, statement, time_format)
        
        if isinstance(df, pd.DataFrame):
            table.append(df)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(create_table, ticker_list, repeat(statement), repeat(time_format))

    table_concat = pd.concat(table)
    # table_concat['amount'] =  pd.to_numeric(table_concat['amount'])

    return table_concat


# Update the list table BEFORE the detail view

r = s.query(Earnings_release.__table__).filter(Earnings_release.release_date >= look_back_date).all()
earnings_df = pd.DataFrame(r)
earnings_df.columns = Earnings_release.__table__.columns.keys()

# 1 - We are not concerned with tickers that are not in our DB
df = earnings_df[earnings_df['last_period_DB'].notna()]

# 2 - Remove all the rows that dont have data on Trend
df = df[df['last_period_M'].notna()]

# 3 - Remove all the rows where DB = N
df = df[df['last_period_DB'] != df.last_period_N]

# 4 - Remove all the rows where db == m
# df = df[df['last_period_DB'] != df['last_period_M']]

print(df)
for row in df.iterrows():

    id_ = row[1][0]
    ticker = row[1][3]
    # LATEST PERIOD M THAT WE HAVE ON OUR DATABASE
    last_period_M_on_record = row[1][7]
    on_DB = row[1][6]
    M_latest = M.latest_ending_period_available(ticker)

    # 5 - 
    if last_period_M_on_record != M_latest:
        pass