# import sys, os



# sys.path.append(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.realpath(
#                 __file__
#             )
#         )
#     )
# )

# from database.database import Database
# from scrapping_sources.Macrotrend import Macrotrend
# from models import Statements_list_table
# import pandas as pd
# import concurrent.futures
# from itertools import repeat


# class Statements_list(Database, Macrotrend):

#     def get_statement_list__DB__(self, ticker):

#         """Returns a dataframe containing all statements present
#          in the database from a particular ticker"""

#         r = self.s.query(
#             Statements_list_table.date,
#             Statements_list_table.ticker,
#             Statements_list_table.statement,
#             Statements_list_table.security_id,
#             # Statements_list_table.statement_id
#         ).where(
#             Statements_list_table.ticker == ticker,
#         ).all()

#         df = pd.DataFrame(r)
#         df.columns = [['date','ticker','statement','security_id']]

#         return df

#     def get_statement_list__M__(self, ticker, statement, time_format):

#         """Generates a statements list from macrotrend based on the arguments:
#             -ticker,
#             -statement,
#             -time_format"""

#         df = self.arrange_data(ticker, statement, time_format)
#         if not df.empty:
#             df = df[['date','ticker', 'statement', 'security_id']].drop_duplicates()
#             df["security_id"] = df["ticker"].map(self.security_id_map())

#             return df

#     def generate_statement_list_multi(self, ticker_list, statement, time_format):

#         table = []

#         def create_table(ticker, statement, time_format):

#             """Creates a table from ticker"""
#             df = self.get_all_statements__M__(ticker, statement, time_format)
            
#             if isinstance(df, pd.DataFrame):
#                 table.append(df)

#         with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#             executor.map(create_table, ticker_list, repeat(statement), repeat(time_format))

#         table_concat = pd.concat(table)
#         # table_concat['amount'] =  pd.to_numeric(table_concat['amount'])

#         return table_concat


#     def get_all_statements__M__(self, ticker):

#         """generates a statement list from Macrotrend with all statements
#         and time formats combined, for a ticker"""

#         table = []

#         for stmnt in self.statements:
#             for t_format in self.time_format:

#                 df = self.get_statement_list__M__(ticker, stmnt, t_format)
#                 table.append(df)

#         results = pd.concat(table)
#         results.columns = [['date','ticker','statement','security_id']]

#         return results

#     def generate_list_update(self, ticker):

#         """Creates a dataframe made up of the difference between DB and M"""

#         db = self.get_statement_list__DB__(ticker)
#         m = self.get_all_statements__M__(ticker)
#         update = pd.concat([db,m]).drop_duplicates(keep=False)

#         return update

#     # def statement_list_mapping(self, ticker, date, statement):

#     #     try:
#     #         # stmnt = self.generate_statement_key(statement, time_format)

#     #         r = self.s.query(
#     #             Statements_list_table.statement_id
#     #         ).where(
#     #             Statements_list_table.ticker == ticker,
#     #             Statements_list_table.date == date, 
#     #             Statements_list_table.statement == statement
#     #         ).all()

#     #         return r[0][0]
#     #     except:
#     #         pass