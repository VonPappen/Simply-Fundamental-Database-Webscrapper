# IN THIS VERSION, WE UPDATE THE STATEMENTS DETAIL AND LIST AT THE SAME TIME


import os, sys

from pandas.core.indexes import period

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(
                __file__
            )
        )
    )
)

from config import DATABASE_URI
from models import Earnings_release, Security, Statements_table_log#, Base, Lambda_logs, 
from scrapping_sources.Macrotrend import Macrotrend
# from earnings_release.earnings_release import last_period_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import datetime

DAY_VARIABLE = 30
look_back_date = str(datetime.date.today() - datetime.timedelta(days=DAY_VARIABLE))

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()

querry = s.query(Security.ticker, Security.id).all()
security_map = {querry[i][0]: querry[i][1] for i, v in zip(range(len(querry)), range(len(querry)))}

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

# FOR USE IN CONJONCTION WITH THE latest_DB/M functions
convert_dict = {
    'date': str,
    'statement': str,
    'ticker': str,
    'security_id': int,
    'line_item': str,
    # 'amount': float
}

def no_table_log(ticker, stmnt, t_format):

    r = s.query(Statements_table_log.__table__).filter(
        Statements_table_log.ticker == ticker,
        Statements_table_log.statement == stmnt,
        Statements_table_log.time_format == t_format,
        Statements_table_log.period == M.latest_ending_period_available(ticker)
    ).all()

    return len(r) == 0

M = Macrotrend()

r = s.query(Earnings_release.__table__).filter(Earnings_release.release_date >= look_back_date).all()
earnings_df = pd.DataFrame(r)
earnings_df.columns = Earnings_release.__table__.columns.keys()

# 1 - We are not concerned with tickers that are not in our DB
df = earnings_df[earnings_df['last_period_DB'].notna()]

# 2 - Remove all the rows that dont have data on Trend
df = df[df['last_period_M'].notna()]

# 3 - Remove all the rows where DB = N
df = df[df['last_period_DB'] != df.last_period_N]

for row in df.iterrows():

    id_ = row[1][0]
    ticker = row[1][3]
    # LATEST PERIOD M THAT WE HAVE ON OUR DATABASE
    last_period_M_on_record = row[1][7]
    on_DB = row[1][6]
    M_latest = M.latest_ending_period_available(ticker)

    if last_period_M_on_record != M_latest:

        print(f"UPDATING EARNINGS TABLE, COLUMN M, FOR {ticker}")
        s.query(Earnings_release.__table__). \
            filter(Earnings_release.id == id_). \
            update({"last_period_M": f"{M_latest}"})
        s.commit()

        print("GETTING STATEMENTS FROM MACROTREND")
        for stmnt in statements:
            for t_format in time_format:

                pass
            # TODO: STATEMENTS_LIST_FUNCTION_IS READY
            # COMBINE BOTH FUNCTIONS IN THIS LOOP
            # TODO: UPDATE THE DEATAIL UPDATE FUNCTION 
            # MAKE SURE IT USES THE SAME LOGIC THAN LIST