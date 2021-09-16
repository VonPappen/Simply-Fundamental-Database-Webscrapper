import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sqlalchemy import create_engine
from config import DATABASE_URI
from scrapping_sources.Finviz import Finviz

engine = create_engine(DATABASE_URI)
tot_sec = Finviz().total_securities()
security_table = Finviz().generate_security_table()
security_table = security_table.sort_values('ticker').reset_index(drop=True)
security_table.to_sql(con=engine, if_exists = 'append', index = False, name='securities_table')