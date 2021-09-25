import requests
from bs4 import BeautifulSoup as bs
# from tqdm import tqdm
import pandas as pd
import time


class Finviz():

    def __init__(self):

        pass

    def total_securities(self, ):

        """Returns the maximum number of securities available on Finviz"""

        url = 'https://finviz.com/screener.ashx?v=152&c=1,2,3,4,5'
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        soup = bs(res.content, features = 'lxml')
        number_of_securities = soup.find_all("td", { 'class' : "count-text"})[0].text.split(' ')[1]
        number_of_securities = int(number_of_securities)
        return number_of_securities

    def generate_security_table(self):
        """Generates a pandas dataframe from finviz based off ticker, company, sector, industry, country"""

        # Get the Finviz Querry parameter
        querry_list = []
        querry_param = 1
        total_finviz_securities = self.total_securities()

        while querry_param <= total_finviz_securities:
            querry_list.append(querry_param)
            querry_param += 20

        ticker   = []
        company  = []
        sector   = []
        industry = []
        country  = []

        print('Starting to fecth...')
        print(querry_list)

        # 
        for i in querry_list:


            time.sleep(1)
            print(i)
            file = f'https://finviz.com/screener.ashx?v=152&c=1,2,3,4,5&r={str(i)}'
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }
            res_status = 0
            while res_status != 200:
                try:
                    res = requests.get(file, headers=headers)
                    res_status = res.status_code
                    data = pd.read_html(res.content)[7]
                    print(res.status_code)
                    [ticker.append(i) for i in data.iloc[1:][0].values]
                    [company.append(i) for i in data.iloc[1:][1].values]
                    [sector.append(i) for i in data.iloc[1:][2].values]
                    [industry.append(i) for i in data.iloc[1:][3].values]
                    [country.append(i) for i in data.iloc[1:][4].values]
                except:
                    pass

        security_table = pd.DataFrame(
            [
                ticker,
                company,
                sector,
                industry,
                country
            ],
            index = [
                'ticker',
                'company',
                'sector',
                'industry',
                'country'
                ]
            ).T

        return security_table
