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

# from statements_list import Statements_list
from database.database import Database
from scrapping_sources.Macrotrend import Macrotrend
import pandas as pd
import concurrent.futures
from itertools import repeat

M = Macrotrend()

ticker_list = Database().ticker_list()
security_map = Database().security_id_map()
# Stmnt_list = Statements_list()

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





def get_statement_list__M__(ticker, statement, time_format):

    """Generates a statements list from macrotrend based on the arguments:
        -ticker,
        -statement,
        -time_format"""

    df = M.arrange_data(ticker, statement, time_format)
    if not df.empty:
        df = df[['date','ticker', 'statement', 'security_id', 'statement_id']].drop_duplicates()
        df["security_id"] = df["ticker"].map(security_map)

        return df

def get_all_statements__M__( ticker):

    """generates a statement list from Macrotrend with all statements
    and time formats combined, for a ticker"""

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

    table = []

    for stmnt in statements:
        for t_format in time_format:

            df = get_statement_list__M__(ticker, stmnt, t_format)
            table.append(df)

    results = pd.concat(table)
    results.columns = [['date','ticker','statement','security_id', 'statement_id']]

    return results

def generate_statement_list_multi(ticker_list):

    table = []

    def create_table(ticker):

        """Creates a table from ticker"""
        df = get_all_statements__M__(ticker)
        
        if isinstance(df, pd.DataFrame):
            table.append(df)

    with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
        executor.map(create_table, ticker_list)#, repeat(statement), repeat(time_format))

    table_concat = pd.concat(table)
    # table_concat['amount'] =  pd.to_numeric(table_concat['amount'])

    return table_concat


# TESTING PURPOSES

# print(generate_statement_list_multi(['AAPL', 'MSFT']))
# print(get_all_statements__M__(['AAPL']))
# print(get_statement_list__M__('AAPL', 'balance-sheet', 'annual'))
