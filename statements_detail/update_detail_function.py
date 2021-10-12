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
from models import Earnings_release, Security,  Statements_table_log, Base
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

M = Macrotrend()

# INDICATE THAT WE ARE CURRENTLY UPDATING A FUNCTION ON lambda_logs
# lambda_function = "ws_update_statements"

# def check_function_status(function):
#     "returns the status of a lambda_function"

#     try:
#         r = s.query(Lambda_logs.status).filter(
#             Lambda_logs.lambda_function    == function,
#             Lambda_logs.date        == datetime.date.today()
#         ).all()

#         return r[0][0]

#     except:

#         return None


def convert_to_ending_period_format(date):

    """Returns """

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

        r = min(period_list_on_db)

        return convert_to_ending_period_format(r)

    except:
        
        return None


def fetch_all_statement(ticker, stmnt, time_format):

    r = s.query(Base.metadata.tables[f'{stmnt.replace("-", "_")}_{time_format}']).where(
        Base.metadata.tables[
            f'{stmnt.replace("-", "_")}_{time_format}'
            ].columns['ticker'] == str(ticker)
        ).all()

    return r


def statement_table_log_entry(ticker, statement, time_format, status, period):

    """Should have _ different forms of status:
        1/ up to date
        2/ updated
        3/ waiting on trend
        4/ no data on trend
        5/ failure"""

    try:
        security_id = security_map[f"{ticker}"]
    except:
        security_id = None

    load = pd.DataFrame(
        [
            {
                "date": str(datetime.date.today()),
                "ticker": f"{ticker}",
                "security_id": security_id,
                "statement": f"{statement}",
                "time_format": time_format,
                "status": status, 
                "period" : period
            }
        ]
    )
    load.to_sql(
        con=engine,
        name="statements_table_log",
        if_exists="append",
        index=False
    )


def latest_M(ticker, stmnt, t_format):

    """Generates a dataframe containing all the available 
    data of a particular ticker from Macrotrend"""

    latest = M.arrange_data(ticker, stmnt, t_format)
    # latest['security_id'] = latest.ticker.map(security_map)
    latest['amount'] = pd.to_numeric(latest['amount'])
    latest = latest.astype(convert_dict)
    
    return latest


def latest_DB(ticker, stmnt, t_format):

    """Genereates a dataframe containing all the available
     data of a particular ticker from the database"""

    results = pd.DataFrame(fetch_all_statement(ticker, stmnt, t_format))

    if not results.empty:

        results.columns = ['id', 'date', 'statement', 'ticker', 'security_id', 'line_item', 'amount']
        # results['security_id'] = results.ticker.map(security_map)
        results = M.move_column(results, 'security_id', 3)
        results = results.astype(convert_dict)

        return results

# print(fetch_all_statement('AAPL','balance-sheet', 'annual'))


################################# FOR TESTING PURPOSES

r = s.query(Earnings_release.__table__).filter(Earnings_release.release_date >= look_back_date).all()
earnings_df = pd.DataFrame(r)
earnings_df.columns = Earnings_release.__table__.columns.keys()

# 1 - We are not concerned with tickers that are not in our DB
df = earnings_df[earnings_df['last_period_DB'].notna()]

# 2 - Remove all the rows that dont have data on Trend
df = df[df['last_period_M'].notna()]

# 3 - Remove all the rows where DB = N
df = df[df['last_period_DB'] != df.last_period_N]

print(df['ticker'])



##################################

def update_db(ticker, stmnt, t_format):

    """Compares the database with Macrotrend
    and update when necessary"""

    # TODO: ATTRIBUTE A SINGLE ENTRY FOR EACH OF THE TICKERS ON THE 
    # STATEMENTS_TABLE_LOG

    in_database = latest_DB(ticker, stmnt, t_format)
    latest = latest_M(ticker, stmnt, t_format)

    # if they are both datafrfames
    if isinstance(in_database, pd.DataFrame) and isinstance(latest, pd.DataFrame):
        
        # if they do not have the same number of rows, an update must tabke place
        if latest.shape[0] != in_database.shape[0]:
        


            # UPDATE THE DATABASE
            in_database['date'] = pd.to_datetime(in_database['date'])
            indb_date_set = set(in_database.date.values)
            latest['date'] = pd.to_datetime(latest.date)
            update_date_set = set(latest.date.values)
            update = latest[latest.date.isin(list(update_date_set - indb_date_set))]
            df = update[['date','ticker', 'statement', 'security_id', 'statement_id']].drop_duplicates()

            print(df)


            # # UPDATE THE CORRESPONDING TABLE
            # update.to_sql(
            #     con=engine, 
            #     name=f"{stmnt.replace('-', '_')}_{t_format}",
            #     if_exists='append',
            #     index=False
            # )

            # in_database = latest_DB(ticker, stmnt, t_format)

            # if latest.shape[0] == in_database.shape[0]:

            #     return "UPDATE SUCCESFUL"

# update_db('')