import pandas as pd
import requests, json, re
from bs4 import BeautifulSoup as bs
import datetime
import concurrent.futures
from itertools import repeat

class Macrotrend():
        
    def get_statement(self, ticker, statement, time_format):

        statement_data = None #default load

        if time_format == 'annual':

            try:
                r = requests.get('https://www.macrotrends.net/stocks/charts/' + ticker + '/' + ticker + '/' + statement)
                print(ticker, r)
                p = re.compile(r'var originalData = (.*);')
                p2 = re.compile(r'datafields:[\s\S]+(\[[\s\S]+?\]),')
                p3 = re.compile(r'\d{4}-\d{2}-\d{2}')
                data = json.loads(p.findall(r.text)[0])
                s = re.sub('\r|\n|\t|\s','',p2.findall(r.text)[0])
                fields = p3.findall(s)
                fields.insert(0, 'field_name') # only headers of interest.
                results = []

                for item in data: #loop initial list of dictionaries
                    row = {}
                    for f in fields: #loop keys of interest to extract from current dictionary
                        if f == 'field_name':  #this is an html value field so needs re-parsing
                            soup2 = bs(item[f],'lxml')
                            row[f] = soup2.select_one('a,span').text
                        else:
                            row[f] = item[f]
                    results.append(row)

                # return pd.DataFrame(results, columns = fields)
                statement_data = pd.DataFrame(results, columns = fields)

                return statement_data
        
            except:
                print(f"No data available for {ticker}, {statement}, annual")
                pass
            # pass
        else:

            try:

                r = requests.get(f'https://www.macrotrends.net/stocks/charts/' + ticker + '/' + ticker + '/' + statement)
                company_name = r.url.split('/')[6]
                r = requests.get(f'https://www.macrotrends.net/stocks/charts/'+ ticker + '/' + company_name + '/' + statement + '?freq=Q')
                print(ticker, r)
                p = re.compile(r'var originalData = (.*);')
                p2 = re.compile(r'datafields:[\s\S]+(\[[\s\S]+?\]),')
                p3 = re.compile(r'\d{4}-\d{2}-\d{2}')
                data = json.loads(p.findall(r.text)[0])
                s = re.sub('\r|\n|\t|\s','',p2.findall(r.text)[0])
                fields = p3.findall(s)
                fields.insert(0, 'field_name') # only headers of interest.
                results = []

                for item in data: #loop initial list of dictionaries
                    row = {}
                    for f in fields: #loop keys of interest to extract from current dictionary
                        if f == 'field_name':  #this is an html value field so needs re-parsing
                            soup2 = bs(item[f],'lxml')
                            row[f] = soup2.select_one('a,span').text
                        else:
                            row[f] = item[f]
                    results.append(row)
                statement_data = pd.DataFrame(results, columns = fields)

                return statement_data

            except:

                print(f"No data available for {ticker}, {statement}, quarterly")

                pass

    def item_amount_unit(ticker, statement, time_format):

        if time_format == "annual":

            r = requests.get('https://www.macrotrends.net/stocks/charts/' + ticker + '/' + ticker + '/' + statement)
            text = r.text
            pattern = re.compile(r"var columnList = (.*);", re.DOTALL)
            matches = pattern.findall(text)
            matches = re.sub("\r|\n|\t",'',  matches[0])
            pattern2 = re.compile(r"'(.*?)'")
            match = pattern2.findall(str(matches))[0]

            return str(match).split(" | ")[1]

        elif time_format == "quarterly":

            r = requests.get(f'https://www.macrotrends.net/stocks/charts/' + ticker + '/' + ticker + '/' + statement)
            company_name = r.url.split('/')[6]
            r = requests.get(f'https://www.macrotrends.net/stocks/charts/'+ ticker + '/' + company_name + '/' + statement + '?freq=Q')
            text = r.text
            pattern = re.compile(r"var columnList = (.*);", re.DOTALL)
            matches = pattern.findall(text)
            matches = re.sub("\r|\n|\t",'',  matches[0])
            pattern2 = re.compile(r"'(.*?)'")
            match = pattern2.findall(str(matches))[0]

            return str(match).split(" | ")[1]

    def move_column(self, df, column, pos):

        col = df[column]
        df.drop(columns=[column],inplace = True)
        df.insert(pos, column, col)

        return df
    
    def generate_statement_key(self, statement, time_format):

        report_formats  = {'quarterly'  : 'Q',
                            'annual'    : 'A'}
        statements      = {'income-statement'       :'IS',
                            'balance-sheet'         :'BS',
                            'cash-flow-statement'   :'CF',
                            'financial-ratios'      :'R'}

        statement_key = statements[statement] + '-' + report_formats[time_format]

        return statement_key

    def arrange_data(self, ticker, statement, time_format):

        data_dict = []
        report_formats = {'quarterly' : 'Q',
                        'annual': 'A'}
        statements = {'income-statement':'IS',
                    'balance-sheet':'BS',
                    'cash-flow-statement':'CF',
                    'financial-ratios':'R'}

        df = self.get_statement(ticker, statement, time_format)

        if isinstance(df, pd.DataFrame):

            for i in df.columns[1:]:
                keys = df[df.columns[0]]
                data = df[i].values
                data = {k:v for k,v in zip(keys, data)}
                date = i
                data['date'] = date
                data['ticker'] = ticker
                data['statement_format'] = statements[statement] + '-' + report_formats[time_format]
                data_dict.append(data)

            df = pd.DataFrame(data_dict)
            df = self.move_column(df, 'date', 0)
            df = self.move_column(df, 'ticker', 1)
            df = self.move_column(df, 'statement_format', 2)

            my_series = []
            line_item = []
            amount = []
            date = []
            ticker = []
            security_id = []
            statement_format = []

            for i in df.iterrows():

                serie = pd.Series(i)[1]
                my_series.append(serie)
                [statement_format.append(serie[2]) for i in range(len(serie.index.values[4:]))]
                # [security_id.append(serie[3]) for i in range(len(serie.index.values[4:]))]
                [line_item.append(i) for i in  serie.index.values[4:]]
                [amount.append(i) for i in serie.values[4:]]
                [date.append(serie[0]) for i in  range(len(serie.index.values[4:]))]
                [ticker.append(serie[1]) for i in range(len(serie.index.values[4:]))]

            data = pd.DataFrame([date, statement_format, ticker, security_id,line_item, amount]).T
            data.columns = ['date','statement','ticker','security_id','line_item','amount']

            return data


    def generate_statement_table_multi(self, ticker_list, statement, time_format):

        table   = []

        for i in ticker_list:

            df = self.arrange_data(i, statement, time_format)

            if isinstance(df, pd.DataFrame):
                table.append(df)
            else:
                pass

        table_concat = pd.concat(table)
        table_concat['amount'] =  pd.to_numeric(table_concat['amount'])
        return table_concat

    def generate_statement_table_multi_threading(self, ticker_list, statement, time_format):

        table = []

        def create_table(ticker, statement, time_format):

            """Creates a table from ticker"""

            ############### WIP
            # for each stmnt
            # for each t_format
                # --------> Create an entry on statement_table
                # ticker | stmnt | time_format | period | security_id | stmnt_id
            ################ 

            df = self.arrange_data(ticker, statement, time_format)
            if isinstance(df, pd.DataFrame):
                table.append(df)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(create_table, ticker_list, repeat(statement), repeat(time_format))

        table_concat = pd.concat(table)
        table_concat['amount'] =  pd.to_numeric(table_concat['amount'])

        return table_concat
    
    def latest_ending_period_available(self, ticker, statement='balance-sheet', time_format='quarterly'):

        try:
            df = self.get_statement(ticker, statement, time_format)
            raw_date = df.columns[1]
            converted_date = datetime.datetime.strptime(str(raw_date), '%Y-%m-%d').strftime("%Y-%m")
        except:
            converted_date = None

        return converted_date
    