from database.database import Database
from scrapping_sources.Macrotrend import Macrotrend

# TODO: Simple script to update last_period_M everyday on Earnings_release_table

# 1 - Get the last 30 days worth of earnings realease
# 2 - Remove rows from the dataframe Nan last_period_DB
# 4 - Remove all the rows where last_period_M is the same as last_period_N
#     |-- we should be left with:
#     |--   tickers that are present in our database
#     |--   tickers that are NOT up to date with Nasdaq

# 4 - Check every day for updates on last_period_M