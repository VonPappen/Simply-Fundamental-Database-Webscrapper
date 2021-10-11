import datetime
import sys, os

from sqlalchemy.sql.expression import table

from initialize_statements_list import get_all_statements__M__

# from updates.statements_updates_v2 import latest_M

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
from models import Security, Earnings_release, Statements_list_table
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


# TODO: CREATE A STATEMENT LIST UPDATE FUNCTION

def latest_DB_list(ticker):

    # Retrieves all the statement list of a ticker
    r = s.query(
        Statements_list_table.security_id,
        Statements_list_table.ticker,
        Statements_list_table.statement,
        Statements_list_table.date,
        Statements_list_table.statement_id
    ).where(
        Statements_list_table.ticker == ticker
    ).all()

    df = pd.DataFrame(r)

    df.columns = ['security_id', 'ticker','statement', 'date', 'statement_id']

    return df

print(get_all_statements__M__('AAPL'))

# print(latest_DB_list('AAPL'))






# def update_db_list(ticker, stmnt, t_format):

#     """Compares the database with Macrotrend
#     and update when necessary"""

#     #  ATTRIBUTE A SINGLE ENTRY FOR EACH OF THE TICKERS ON THE 
#     # STATEMENTS_TABLE_LOG

#     in_database = latest_DB(ticker, stmnt, t_format)
#     latest = latest_M(ticker, stmnt, t_format)




s.close_all()