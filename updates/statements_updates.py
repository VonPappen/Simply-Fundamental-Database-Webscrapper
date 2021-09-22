
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
from models import Earnings_release, Security, Base
from scrapping_sources.Macrotrend import Macrotrend
# from earnings_release.earnings_release import last_period_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import datetime

DAY_VARIABLE = 14
look_back_date = str(datetime.date.today() - datetime.timedelta(days=DAY_VARIABLE))

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()

querry = s.query(Security.ticker, Security.id).all()
security_map = {querry[i][0]: querry[i][1] for i, v in zip(range(len(querry)), range(len(querry)))}

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

M = Macrotrend()


r = s.query(Earnings_release.__table__).filter(Earnings_release.date >= look_back_date).all()
earnings_df = pd.DataFrame(r)
earnings_df.columns = Earnings_release.__table__.columns.keys()
df = earnings_df[earnings_df['last_period_DB'].notna()]
df = df[df['last_period_M'].notna()]

# 1 - Remove all the rows where DB = N
df = df[df['last_period_DB'] != df.last_period_N]

def convert_to_ending_period_format(date):
    """Returns """
    result = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime("%Y-%m")
    return result

def last_period_db(ticker):
    try:
        r = s.query(Base.metadata.tables['income_statement_quarterly'].columns['date']).where(
            Base.metadata.tables['income_statement_quarterly'].columns['ticker'] == str(ticker)
        ).all()
        r.sort(reverse=True)
        r =  str(r[0][0])
        return convert_to_ending_period_format(r)
    except:
        return None

def fetch_all_statement(ticker, stmnt, time_format):

    r = s.query(Base.metadata.tables[f'{stmnt}_{time_format}']).where(\
            Base.metadata.tables[f'{stmnt}_{time_format}'].columns['ticker'] ==str(ticker)).all()
    return r

def update_db(ticker):

    for stmnt in statements:
        for t_format in time_format:

            latest = M.arrange_data(ticker, stmnt, t_format)
            in_database = pd.DataFrame(fetch_all_statement(ticker, stmnt, t_format))

            try:
                in_database.columns = ['date','statement','ticker','line_item', 'amount']
                in_database['security_id'] = in_database.ticker.map(security_map)
                in_database = M.move_column(in_database, 'security_id', 3)
                latest['security_id'] = latest.ticker.map(security_map)
                convert_dict = {
                    'date': str,
                    'statement': str,
                    'ticker': str,
                    'security_id': int,
                    'line_item': str,
                    'amount': float
                }

                in_database = in_database.astype(convert_dict)
                latest = latest.astype(convert_dict)

            except:

                print("Something went wrong in the dataframe creation")

            if isinstance(in_database, pd.DataFrame) and isinstance(latest, pd.DataFrame):

                if latest.shape[0] == in_database.shape[0]:

                    print(f"Security {ticker} is already up to date")

                else:

                    in_database['date'] = pd.to_datetime(in_database.date)
                    indb_date_set = set(in_database.date.values)
                    latest['date'] = pd.to_datetime(latest.date)
                    update_date_set = set(latest.date.values)
                    update = latest[latest.date.isin(list(update_date_set - indb_date_set))]
                    
                    update.to_sql(con = engine, name=f"{stmnt.replace('-','_')}_{time_format}", if_exists='append', index=False)
                    
            elif not isinstance(in_database, pd.DataFrame):

                print(f"Security {ticker} not in database")

            else:

                print(f"NO data available on Macrotrend for {ticker}")

for row in df.iterrows():

    id_ = row[1][0]
    print(id_)
    ticker = row[1][2]
    last_period_M_on_record = row[1][6]
    on_DB = row[1][5]
    M_latest = M.latest_ending_period_available(ticker)
    print(last_period_M_on_record == M_latest)

    if last_period_M_on_record != M_latest:
        print("MARKER 1")

        # UPDATE EARNINGS TABLE M
        s.query(Earnings_release.__table__).\
            filter(Earnings_release.id == id_).\
            update({"last_period_M": f"{M_latest}"})
        s.commit()

        # GET THE STATEMENTS FROM MACROTREND AND POPULATE DB
        update_db(ticker)

        #  VERIFY AND IF SUCCESFUL, UPDATE EARNINGS TABLE
        if last_period_db(ticker) == on_DB:
            print("MARKER 2")
            s.query(Earnings_release.__table__).\
                filter(Earnings_release.id == id_).\
                update({"last_period_DB": f"{last_period_db(ticker)}"})
            s.commit()

        pass

    # IF THE DATE ON THE DATABASE IS NOT THE SAME AS THE DATE ON M
    # POPULATE THE DATABASE WITH THE MISSING DATA
    if on_DB != last_period_M_on_record:
        print("MARKER 3")

        update_db(ticker)



s.close_all()