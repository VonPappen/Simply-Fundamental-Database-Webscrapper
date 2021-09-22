import pandas as pd
import requests, json
import datetime
from bs4 import BeautifulSoup

class Nasdaq:

    def __init__(self, 
        url=r"https://api.nasdaq.com/api/calendar/earnings",
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}):

        self.url = url
        self.headers = headers
        pass

    def earnings_release(self, date, timeout_=5):
        """ Returns the list of released at the specified date 
        date must be in the following format:
        YYYY-MM-DD
        """
        
        res = requests.get(self.url + f'?date={date}', timeout= timeout_, headers = self.headers)
        # print(api)
        jres = json.loads(res.content)
        df = pd.DataFrame(jres['data']['rows'])

        return df

    def earnings_release_tickers(self, date):

        df = self.earnings_release(date)
        return df.symbol.values

    def latest_ending_period_available(self, ticker, date):

        df = self.earnings_release(date=date)

        nsdq_period_ending = df[df.symbol == ticker]['fiscalQuarterEnding']
        convert_nsq_strftime = datetime.datetime.strptime(nsdq_period_ending, '%b/%Y').strftime("%Y-%m")

        return convert_nsq_strftime


# scrapper = Nasdaq()

# raw_date = scrapper.latest_ending_period_available('KMX', datetime.date.today(), 'balance-sheet', 'quarterly')
# print(raw_date)
# print(scrapper.earnings_release(str(datetime.date.today()), 5))



# mytickers_to_up