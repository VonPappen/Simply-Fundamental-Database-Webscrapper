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



# from models import Statements_list_table
from models import Security, Earnings_release
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
import datetime
import pandas as pd

class Database():

    def __init__(
        self,
        USERNAME        = 'postgres',
        HOST            = 'database-webscrap.ccaaerr6cq44.eu-west-3.rds.amazonaws.com',
        DATABASE_NAME   = 'webscrapping',
        PASSWORD        = 'postgres5678',
        PORT            = 5432
    ):

        self.USERNAME= USERNAME
        self.HOST=HOST
        self.DATABASE_NAME= DATABASE_NAME
        self.PASSWORD= PASSWORD
        self.PORT=PORT
        self.DATABASE_URI = f"postgresql+psycopg2://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"
        self.engine = create_engine(self.DATABASE_URI)
        self.session = sessionmaker(bind= self.engine)
        self.s = self.session()
        self.statements = [
            'income-statement',
            'balance-sheet',
            'cash-flow-statement',
            'financial-ratios'
        ]
        self.time_format = [
            'annual',
            'quarterly'
        ]

    def security_id_map(self):
        r = self.s.query(Security.ticker, Security.id).all()
        sec_id_map = {i[0]:i[1] for i in r}

        return sec_id_map

    def close_all(self):
        self.s.close_all()

    def ticker_list(self):

        tickers = self.s.query(Security.ticker).all()
        tickers_list = [i[0] for i in tickers]

        return tickers_list

    
print(Database().security_id_map())