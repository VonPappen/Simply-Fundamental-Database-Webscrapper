#!usr/bin/env python3

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

from sqlalchemy import create_engine
from config import DATABASE_URI
from scrapping_sources.Finviz import Finviz
import pandas as pd
import datetime 

engine = create_engine(DATABASE_URI)
tot_sec = Finviz().total_securities()
security_table = Finviz().generate_security_table()
security_table = security_table.sort_values('ticker').reset_index(drop=True)
security_table.to_sql(con=engine, if_exists = 'append', index = False, name='securities_table')

load = pd.DataFrame(
    [
        {
            "date":str(datetime.date.today()),
            "log":"updated",
            "status":"INITIALIZED",
            "added": f"added {security_table.shape[0]} securities on initialization"
        }
    ]
)
load.to_sql(con=engine, name="securities_table_log", index=False, if_exists="append")