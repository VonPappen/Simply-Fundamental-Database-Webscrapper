from initialize_list_function import generate_statement_list_multi, ticker_list
from sqlalchemy import create_engine
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)


df = generate_statement_list_multi(ticker_list)
df.columns = ['date', 'ticker','statement','security_id', 'statement_id']
df.to_sql(con = engine, name="statements_list_table", if_exists='append', index=False)