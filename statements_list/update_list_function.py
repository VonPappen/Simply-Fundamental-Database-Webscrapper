import datetime
import sys, os

from sqlalchemy.sql.expression import table

from initialize_list_function import get_all_statements__M__

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


def update_statement_list(ticker):

    """Compares the database with Macrotrend
    and update when necessary"""


    in_database_list = latest_DB_list(ticker)
    latest_list = get_all_statements__M__(ticker)

    # if they are both datafrfames
    if isinstance(in_database_list, pd.DataFrame) and isinstance(latest_list, pd.DataFrame):
        
        # if they do not have the same number of rows, an update must tabke place
        if latest_list.shape[0] != in_database_list.shape[0]:


            # format both dataframe 
            in_database_list['date'] = pd.to_datetime(in_database_list['date'])
            latest_list['date'] = pd.to_datetime(latest_list.date)

            # create a date set for both dataframe
            indb_date_set = set(in_database_list.date.values)
            update_date_set = set(latest_list.date.values)
            # extract the update based on date diference
            update = latest_list[latest_list.date.isin(list(update_date_set - indb_date_set))]

            # UPDATE THE CORRESPONDING TABLE
            update.to_sql(
                con=engine, 
                name=f"statement_list_table",
                if_exists='append',
                index=False
            )

            # CHECK IF THE UPDATE IS SUCCESFUL:
            in_database_list = latest_DB_list(ticker)

            if latest_list.shape[0] == in_database_list.shape[0]:

                return "UPDATE SUCCESFUL"


s.close_all()