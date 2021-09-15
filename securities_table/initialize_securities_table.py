#!/usr/bin/env python3

import sys
import os

# sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(os.path.curdir)

import pandas as pd
from scrapping_sources.Finviz import Finviz
from database.database_class import Database

my_db = Database()
mysql_statement = """CREATE TABLE IF NOT EXISTS securities_table 
    (security_id INT(100) NOT NULL AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    company VARCHAR(255) NOT NULL,
    sector VARCHAR(255) NOT NULL,
    industry VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    PRIMARY KEY(security_id),
    CONSTRAINT unique_cie UNIQUE (ticker, company));                                                      
"""

my_db.execute(mysql_statement)

tot_sec = Finviz().total_securities()

security_table = Finviz().generate_security_table()

security_table = security_table.sort_values('ticker').reset_index(drop=True)

engine = my_db.create_engine()
security_table.to_sql(con=engine, if_exists = 'append', index = False, name='securities_table')