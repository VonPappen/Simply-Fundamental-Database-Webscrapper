
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
print(df)

for row in df.iterrows():

    id_ = row[1][0]
    print(id_)
    ticker = row[1][2]
    last_period_M_on_record = row[1][6]
    on_DB = row[1][5]
    M_latest = M.latest_ending_period_available(ticker)
    print(last_period_M_on_record == M_latest)
    if last_period_M_on_record != M_latest:

        # UPDATE EARNINGS TABLE M
        s.query(Earnings_release.__table__).\
            filter(Earnings_release.id == id_).\
            update({"last_period_M": f"{str(M_latest)}"})
        s.commit()

        # GET THE STATEMENTS FROM MACROTREND AND POPULATE DB
        for stmnt in statements:
            for t_format in time_format:

                latest = M.arrange_data(ticker, stmnt, t_format)
                # in_database = pd.DataFrame(my_db.fetch_all_statement(tick, stmnt, time_format))

                try:

                    
                    latest = M.arrange_data(ticker, stmnt, t_format)
                    latest['security_id'] = latest.ticker.map(security_map)
                    convert_dict = {
                        'date': str,
                        'statement': str,
                        'ticker': str,
                        'security_id': int,
                        'line_item': str,
                        'amount': float
                    }
                    latest = latest.astype(convert_dict)

                except:

                

        #  VERIFY

        # UPDATE EARNINGS TABLE DB

        pass

    # IF THE DATE ON THE DATABASE IS NOT THE SAME AS THE DATE ON M
    # POPULATE THE DATABASE WITH THE MISSING DATA (create a set)
    if on_DB != last_period_M_on_record:

        pass



s.close_all()