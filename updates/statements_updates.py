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

from config import DATABASE_URI
from models import Earnings_release, Security, Base, Lambda_logs
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

M = Macrotrend()

# INDICATE THAT WE ARE CURRENTLY UPDATING A FUNCTION ON lambda_logs
lambda_function = "ws_update_statements"

def check_function_status(function):
    "returns the status of a lambda_function"

    try:
        r = s.query(Lambda_logs.status).filter(
            Lambda_logs.lambda_function    == function,
            Lambda_logs.date        == datetime.date.today()
        ).all()
        return r[0][0]
    except:
        return None


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

        r = max(period_list_on_db)

        return convert_to_ending_period_format(r)

    except:
        
        return None


def fetch_all_statement(ticker, stmnt, time_format):
    r = s.query(Base.metadata.tables[f'{stmnt.replace("-", "_")}_{time_format}']).where(
        Base.metadata.tables[f'{stmnt.replace("-", "_")}_{time_format}'].columns['ticker'] == str(ticker)).all()
    return r


def statement_table_log(ticker, statement, time_format, status):

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
                "status": status
            }
        ]
    )
    load.to_sql(
        con=engine,
        name="statements_table_log",
        if_exists="append",
        index=False
    )


# def statement_table_log_status(ticker, stmnt, t_format):
#     """Retrieves the current status of a particular 
#     statement_table_log_entry
#     For the date parameter, get a query that returns the closest date to today
#     """

#     period = M.latest_ending_period_available(ticker)

#     result = s.query(Statements_table_log.period). \
#             filter(
#                 (Statements_table_log.statement == stmnt),
#                 (Statements_table_log.ticker == ticker),
#                 (Statements_table_log.time_format == t_format),
#                 (Statements_table_log.period == period)
#             ).order_by(Statements_table_log.date.desc()).limit(1).all()

#     return result[0][0]



def update_db(ticker, stmnt, t_format):

    latest = M.arrange_data(ticker, stmnt, t_format)
    in_database = pd.DataFrame(fetch_all_statement(ticker, stmnt, t_format))
    print(f"IN DATABASE {ticker} {stmnt} {t_format}", in_database)

    if not in_database.empty:

        try:
            in_database.columns = ['id', 'date', 'statement', 'ticker', 'security_id', 'line_item', 'amount']
            in_database['security_id'] = in_database.ticker.map(security_map)
            in_database = M.move_column(in_database, 'security_id', 3)
            print(in_database)
            latest['security_id'] = latest.ticker.map(security_map)
            latest['amount'] = pd.to_numeric(latest['amount'])
            convert_dict = {
                'date': str,
                'statement': str,
                'ticker': str,
                'security_id': int,
                'line_item': str,
                # 'amount': float
            }

            in_database = in_database.astype(convert_dict)
            latest = latest.astype(convert_dict)

        except:

            print("Something went wrong in the dataframe creation")

        if isinstance(in_database, pd.DataFrame) and isinstance(latest, pd.DataFrame):

            if latest.shape[0] == in_database.shape[0]:

                print(f"Security {ticker} is already up to date")
                statement_table_log(ticker, stmnt, t_format, status="up to date")

            else:

                in_database['date'] = pd.to_datetime(in_database['date'])
                indb_date_set = set(in_database.date.values)
                latest['date'] = pd.to_datetime(latest.date)
                update_date_set = set(latest.date.values)
                update = latest[latest.date.isin(list(update_date_set - indb_date_set))]
                # UPDATE THE CORRESPONDING TABLE
                update.to_sql(con=engine, name=f"{stmnt.replace('-', '_')}_{t_format}", if_exists='append', index=False)
                # UPDATE THE STATEMENTS TABLE LOG
                statement_table_log(ticker, stmnt, t_format, status="updated")

        elif not isinstance(in_database, pd.DataFrame):

            statement_table_log(
                ticker,
                stmnt,
                t_format,
                status=f"{ticker} Not in Database"
            )

        else:

            statement_table_log(
                ticker,
                stmnt,
                t_format,
                status=f"{ticker} no data availble on M"
            )

    else:
        latest['security_id'] = latest.ticker.map(security_map)
        latest['amount'] = pd.to_numeric(latest['amount'])
        convert_dict = {
            'date': str,
            'statement': str,
            'ticker': str,
            'security_id': int,
            'line_item': str,
            # 'amount': float
        }
        latest = latest.astype(convert_dict)
        latest['date'] = pd.to_datetime(latest.date)
        latest.to_sql(con=engine, name=f"{stmnt.replace('-', '_')}_{t_format}", if_exists='append', index=False)
        # UPDATE THE STATEMENTS TABLE LOG
        # TODO: Move this function to the bottom of a foor loop
        statement_table_log(ticker, stmnt, t_format, status="updated")


if check_function_status(lambda_function) == "Updating...":

    pass

elif check_function_status(lambda_function) == "Completed.":

    pass

else:

    load = pd.DataFrame(
        [
            {
                "date": str(datetime.date.today()),
                "lambda_function" : lambda_function,
                "status": "Updating..."
            }
        ]
    )
    load.to_sql(
        con=engine,
        name="lambda_logs",
        if_exists="append",
        index=False
    )


    r = s.query(Earnings_release.__table__).filter(Earnings_release.release_date >= look_back_date).all()
    earnings_df = pd.DataFrame(r)
    print(earnings_df)
    earnings_df.columns = Earnings_release.__table__.columns.keys()
    df = earnings_df[earnings_df['last_period_DB'].notna()]

    # 1 - Remove all the rows that dont have data on Trend
    df = df[df['last_period_M'].notna()]

    # 2 - Remove all the rows where DB = N
    df = df[df['last_period_DB'] != df.last_period_N]

    for row in df.iterrows():

        id_ = row[1][0]
        print(id_)
        ticker = row[1][3]
        last_period_M_on_record = row[1][7]
        on_DB = row[1][6]
        M_latest = M.latest_ending_period_available(ticker)
        print(last_period_M_on_record == M_latest)

        if last_period_M_on_record != M_latest:
            print("MARKER 1")

            # UPDATE EARNINGS TABLE M
            s.query(Earnings_release.__table__). \
                filter(Earnings_release.id == id_). \
                update({"last_period_M": f"{M_latest}"})
            s.commit()

            # GET THE STATEMENTS FROM MACROTREND AND POPULATE DB
            for stmnt in statements:
                for t_format in time_format:
                    update_db(ticker, stmnt, t_format)
                    # statement_table_log(ticker, stmnt, t_format, status="updated")

                #  VERIFY, IF SUCCESFUL, UPDATE EARNINGS TABLE AND STATEMENTS TABLE LOG
            s.query(Earnings_release.__table__). \
                filter(Earnings_release.id == id_). \
                update({"last_period_DB": f"{last_period_db(ticker)}"})
            s.commit()

            pass

        if on_DB == last_period_M_on_record:
            pass

        # IF THE DATE ON THE DATABASE IS NOT THE SAME AS THE DATE ON M
        # POPULATE THE DATABASE WITH THE MISSING DATA
        if on_DB != last_period_M_on_record:
            print("MARKER 3")
            for stmnt in statements:
                for t_format in time_format:
                    update_db(ticker, stmnt, t_format)
            # ONCE THIS IS DONE, UPDATE THE EARNINGS TABLE
            s.query(Earnings_release.__table__). \
                filter(Earnings_release.id == id_). \
                update({"last_period_DB": f"{last_period_db(ticker)}"})
            s.commit()
    
    # UPDATE THE LAMBDA LOGS:
    s.query(Lambda_logs.__table__).filter(
        Lambda_logs.date == datetime.date.today(),
        Lambda_logs.lambda_function == lambda_function
    ).update(
        {
            "status": "Completed.",
        }
    )

    s.commit()

s.close_all()