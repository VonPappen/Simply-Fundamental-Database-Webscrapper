INITIALIZATION:
____________________

1/ To initiate the Database, we first generate a list of securities based on Finviz
(see securities_table/initiate_securities_table.py and scrapping_sources/Finviz.py)
--> We populate the securities_table

2/ The second phase of the initialization process involves Macrotrend Website:
(see updates/statements_updates.py and scrapping_sources/Macrotrend)
--> We iterrate over the list of securities previously collected during the first step
and see if we can gather informations thanks to the Macrotrend Webscrapper 
--> We generate a table for each statements(Balance-sheet, Income-statement, Cash-Flow +Financial ratios)
and for all time format (annual (10-K forms) and quarterly (10-Q forms))

our database now consists of:

    - securities_table
    - income_statement_annual
    - income_statement_quarterly
    - balance_sheet_annual
    - balance_sheet_quarterly
    - cash_flow_statement_annual
    - cash_flow_statement_quarterly
    - financial_ratios_annual
    - financial_ratios_quarterly

3/ We will also initialize the earnings_release_table and collect the last 30 days earnings release 
data to set a base for the upcoming updates
(see earnings_release/initialize_earningns_release.py and webscrapping_sources/Nasdaq.py)
--> We populate the earnings_release_table with data collected over 30 days prior
to today's date


UPDATING THE DATABASE:
____________________

1/ The entry point of the update starts with a webscrapping of the Nasdaq Website
to see what earnings release came out today. the update is set every day through a cron job with
the eanings_release.py file

2/ once the table is updated, we iterate through the list of securities that had their earnings 
released during the last 30 days. We then follow a simple rule

    --> if the last period available from Nasdaq doesnt match what we have on record, we wait until 
    Macrotrend has the Data ready for us
    --> If the last period from Nasdaq and Macrotrend match, we update the database when possible 
    and the corresponding rows of the earnings_release_table


#### NEXT STEP ---> GET IT DOCKER-READY

OTHER APPROACH --> USE AWS LAMBDA FOR THE CRONJOB