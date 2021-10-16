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
from models import Earnings_release, Security, Base, Statements_table_log
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
lambda_function = "ws_update_statements"

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
    print(results)

    if not results.empty:

        results.columns = ['id', 'date', 'statement', 'ticker', 'security_id', 'line_item', 'amount', 'statement_id']
        # results['security_id'] = results.ticker.map(security_map)
        results = M.move_column(results, 'security_id', 3)
        results = results.astype(convert_dict)

        return results


def no_table_log(ticker, stmnt, t_format):

    r = s.query(Statements_table_log.__table__).filter(
        Statements_table_log.ticker == ticker,
        Statements_table_log.statement == stmnt,
        Statements_table_log.time_format == t_format,
        Statements_table_log.period == M.latest_ending_period_available(ticker)
    ).all()

    return len(r) == 0

def update_statements_log_entry(ticker, stmnt, t_format, period, status):


    s.query(Statements_table_log.__table__).filter(
        Statements_table_log.ticker == ticker,
        Statements_table_log.statement == stmnt,
        Statements_table_log.time_format == t_format,
        Statements_table_log.period == period). \
        update({"status": f"{status}"})
    s.commit()


    pass


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

            df.to_sql(
                con=engine, 
                name="statements_list_table",
                if_exists='append',
                index=False
            )

            # UPDATE THE CORRESPONDING TABLE
            update.to_sql(
                con=engine, 
                name=f"{stmnt.replace('-', '_')}_{t_format}",
                if_exists='append',
                index=False
            )
        
    # elif not isinstance(in_database, pd.DataFrame):

    #     # THIS SHOULDNT HAPPEN BUT IT IS STILL HERE JUST IN CASE
    #     # THE TICKERS LIST THAT WILL GO THROUGH THIS FUNCTION WILL BE 
    #     # COMING FROM THE DATABASE
    #     # COULD ALSO BE USEFUL FOR FUTURE IMPROVEMENTS

    #     latest['security_id'] = latest.ticker.map(security_map)
    #     latest['amount'] = pd.to_numeric(latest['amount'])
    #     convert_dict = {
    #         'date': str,
    #         'statement': str,
    #         'ticker': str,
    #         'security_id': int,
    #         'line_item': str,
    #         # 'amount': float
    #     }
    #     latest = latest.astype(convert_dict)
    #     latest['date'] = pd.to_datetime(latest.date)
    #     latest.to_sql(
    #         con=engine,
    #         name=f"{stmnt.replace('-', '_')}_{t_format}",
    #         if_exists='append',
    #         index=False
    #     )

    #     statement_table_log_entry(
    #         ticker,
    #         stmnt,
    #         t_format,
    #         status=f"{ticker} Not in Database",
    #         period= M.latest_ending_period_available(ticker, stmnt, t_format)
    #     )

    # elif not isinstance(latest, pd.DataFrame):

    #     # THIS SHOULD NOT HAPPEN EITHER BECAUSE WE WILL BE FILTERING 
    #     # ALL THE TICKERS THAT WILL HAVE DATA ON TREND BEFOREHAND

    #     statement_table_log_entry(
    #         ticker,
    #         stmnt,
    #         t_format,
    #         status=f"No data availble on M",
    #         period=None
    #     )
 

r = s.query(Earnings_release.__table__).filter(Earnings_release.release_date >= look_back_date).all()
earnings_df = pd.DataFrame(r)
earnings_df.columns = Earnings_release.__table__.columns.keys()

# 1 - We are not concerned with tickers that are not in our DB
df = earnings_df[earnings_df['last_period_DB'].notna()]

# 2 - Remove all the rows that dont have data on Trend
df = df[df['last_period_M'].notna()]

# 3 - Remove all the rows where DB = N
df = df[df['last_period_DB'] != df.last_period_N]

print(df)
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
                
                # ONLY PROCEED TO UPDATE THE DATABASE IF:
                # (TICKER, STMNT, T_FORMAT AND PERIOD) DOESN"T HAVE AN ENTRY ON THE TABLE
                # --- IF IT DOES, PASS
                if no_table_log(ticker, stmnt, t_format):
                    print(f"UPDATING {ticker} with {stmnt}, {t_format}")

                    # TODO: INSERT STATEMENT LIST UPDATE FUNCTION HERE
                    # BY DOING SO, WE WOULD NEED TO INCORPORATE A STATEMENT_ID COLUMN IN THE
                    # UPDATE FUNCTION BELOW

                    # TODO: CREATE A METHOD ALLOWING TO MAP A STATEMENT_ID

                    update_db(ticker, stmnt, t_format)
                    # TODO: CHECK IF THE UPDATE HAS WORKED
                    statement_table_log_entry(
                        ticker, 
                        stmnt, 
                        t_format, 
                        status="updated",
                        period=M.latest_ending_period_available(ticker))

        print(f"UPDATING EARNINGS_TABLE FOR {ticker}")
        s.query(Earnings_release.__table__). \
            filter(Earnings_release.id == id_). \
            update({"last_period_DB": f"{last_period_db(ticker)}"})
        s.commit()

    # IF THE DATE ON THE DATABASE IS NOT THE SAME AS THE DATE ON M
    # POPULATE THE DATABASE WITH THE MISSING DATA
    if on_DB != last_period_M_on_record:
        if on_DB != 'None':
            print(f"TICKER: {ticker}, ON_DB: {on_DB}, LAST_M_PERIOD_ON_RECORD: {last_period_M_on_record}")
            for stmnt in statements:
                for t_format in time_format:
                    if no_table_log(ticker, stmnt, t_format):
                        update_db(ticker, stmnt, t_format)
                        statement_table_log_entry(
                            ticker, 
                            stmnt, 
                            t_format, 
                            status="updated",
                            period=M.latest_ending_period_available(ticker))


            # ONCE THIS IS DONE, UPDATE THE EARNINGS TABLE
            s.query(Earnings_release.__table__). \
                filter(Earnings_release.id == id_). \
                update({"last_period_DB": f"{last_period_db(ticker)}"})
            s.commit()

s.close_all()