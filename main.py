import pprint
import requests
import os
from dotenv import load_dotenv, dotenv_values
import datetime

load_dotenv()

AV_url = os.getenv('alpha_vantage_url')
AV_api_key = os.getenv('alphaV_api_key_second')

NAPI_url = os.getenv('newsapi_url')
NAPI_api_key = os.getenv('newsapi_key')

STOCK = "ELF"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"

# Function to call the API and get data to work with
def call_stock_api(stock, api_key, endpoint):

    stock_params = {
        'function': 'Time_Series_Daily',
        'symbol': stock,
        'apikey': api_key,

    }

    stock_call = requests.get(endpoint, params=stock_params)
    stock_call.raise_for_status()
    dataS = stock_call.json()

    print(dataS)

    one_day_before_yesterday = round(float(dataS['Time Series (Daily)']['2024-05-21']['4. close']))
    yesterday = round(float(dataS['Time Series (Daily)']['2024-05-22']['4. close']))

    return yesterday, one_day_before_yesterday

# Function to find if the price has made a sufficient movement
def find_sufficient_movements(day, day_before):
    a = .05
    b = a * day_before
    lower = day_before - b
    higher = day_before + b

    if day > day_before and day > higher:
        diff = day - day_before
        direction = 'up'
        return day, diff, direction
    elif day < day_before and day < lower:
        diff = day_before - day
        direction = 'down'
        return day, diff, direction
    else:
        diff = 'stable'
        direction = 'stable'
        return day, diff, direction


# yesterday, day_before = call_stock_api(STOCK, AV_api_key, STOCK_ENDPOINT)
#
# days_price, difference, direction = find_sufficient_movements(yesterday, day_before)


# news start

today = datetime.date.today()
old = today - datetime.timedelta(days=10)

def find_stories(stock):
    news_params = {
        'q': 'Tesla',
        'pageSize': 3,
        'sortBy': 'popularity',
        'apikey': NAPI_api_key
    }

    grab_news = requests.get(NEWS_ENDPOINT, params=news_params)
    grab_news.raise_for_status()
    dataN = grab_news.json()

    article_one = (f'Title: {dataN['articles'][0]['title']}\nSource: {dataN['articles'][0]['source']['name']}\nLink: {dataN['articles'][0]['url']}\n')

    article_two = (f'Title: {dataN['articles'][1]['title']}\nSource: {dataN['articles'][1]['source']['name']}\nLink: {dataN['articles'][1]['url']}\n')

    article_three = (f'Title: {dataN['articles'][2]['title']}\nSource: {dataN['articles'][2]['source']['name']}\nLink: {dataN['articles'][2]['url']}\n')

    return article_one, article_two, article_three

a, b, c = find_stories('TSLA')





# pprint.pp(article_one)


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.





## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

