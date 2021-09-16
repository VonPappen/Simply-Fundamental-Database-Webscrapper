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
print(os.path.curdir)

from scrapping_sources.Macrotrend import Macrotrend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Security
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()
r = s.query(Security.ticker, Security.id).all()
sec_id_map = {i[0]:i[1] for i in r}
scrapper = Macrotrend()

def populate_database(ticker_list):

    """ 
    Pass in a list as parameter 
    - populates the database without differentiating the different time formats and statements
    """

    statements = [
        'income-statement',
        'balance-sheet',
        'cash-flow-statement',
        'financial-ratios'
    ]
    report_formats = [
        'annual', 
        'quarterly'
    ]

    for stmnt in statements:
        for report_format in report_formats:
            df = scrapper.generate_statement_table_multi_threading(ticker_list, stmnt, report_format)
            df['security_id'] = df.ticker.map(sec_id_map)
            df.to_sql(con = engine, name=f"{stmnt.replace('-','_')}_{report_format}", if_exists='append', index=False)


tickers_query = s.query(Security.ticker).all()
tickers_ = [i[0] for i in tickers_query]

# separate into multiple small jobs
def chunks(lst, n):
    chunk_list = []
    for i in range(0, len(lst), n):
        chunk_list.append(lst[i:i + n])
    return chunk_list

tickers_list_chunks = chunks(tickers_, 100)

for chunk in tickers_list_chunks:
    print(chunk)
    populate_database(chunk)

s.close_all()