from initialize_list_function import generate_statement_list_multi, ticker_list, Stmnt_list


df = generate_statement_list_multi(ticker_list)
df.columns = ['date', 'ticker','statement','security_id', 'statement_id']
df.to_sql(con = Stmnt_list.engine, name="statements_list_table", if_exists='append', index=False)