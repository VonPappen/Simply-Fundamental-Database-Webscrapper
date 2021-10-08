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
from models import Security
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


# for ticker in tickers_list:
#     for stmnt in statements:
#         for t_format in time_format:
#             table_list = []
#             try:
#                 df = generate_statement_list(ticker, stmnt, t_format)
#                 table_list.append(df)
#             except:
#                 pass
# print(pd.concat(table))

# print(generate_statement_list("MSFT","income-statement", "quarterly"))







def generate_statement_list_multi(ticker_list, statement, time_format):

    table = []

    def create_table(ticker, statement, time_format):

        """Creates a table from ticker"""

        ############### WIP
        # for each stmnt
        # for each t_format
            # --------> Create an entry on statement_table
            # ticker | stmnt | time_format | period | security_id | stmnt_id
        ################ 

        df = generate_statement_list(ticker, statement, time_format)
        if isinstance(df, pd.DataFrame):
            table.append(df)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(create_table, ticker_list, repeat(statement), repeat(time_format))

    table_concat = pd.concat(table)
    # table_concat['amount'] =  pd.to_numeric(table_concat['amount'])

    return table_concat


for stmnt in statements:
    for t_format in time_format:

        df = generate_statement_list_multi(tickers_list, stmnt, t_format)

df.to_sql(con = engine, name="statements_list_table", if_exists='append', index=False)