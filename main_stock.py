import pprint
import requests
import os
from dotenv import load_dotenv, dotenv_values
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

# Accounts and keys

AV_url = os.getenv('alpha_vantage_url')
AV_api_key = os.getenv('alphaV_api_key_second')

NAPI_url = os.getenv('newsapi_url')
NAPI_api_key = os.getenv('newsapi_key')

gmail = os.getenv('burner_gmail')
gmail_api_key = os.getenv('gmail_app_pass')

# Constants

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today = datetime.date.today()
old = today - datetime.timedelta(days=10)

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
    dataS = stock_call.json()['Time Series (Daily)']
    dataS_list = [value for (key, value) in dataS.items()]
    yesterday_data = dataS_list[0]
    yesterday_data_plus = dataS_list[1]

    one_day_before_yesterday = round(float(yesterday_data_plus['4. close']))
    yesterday = round(float(yesterday_data['4. close']))

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

# Function for to check percentage of move and return with an arrow
def find_move_percent(day, difference, direction):
    percentage = (int(difference) / int(day)) * 100
    arrow = ''
    if direction == 'up':
        arrow = '\u2191'
    else:
        arrow = '\u2193'

    return f'{arrow} {percentage}%'


price_yesterday, price_day_before = call_stock_api(STOCK, AV_api_key, STOCK_ENDPOINT)

days_price, difference, direction = find_sufficient_movements(price_yesterday, price_day_before)

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

art_one, art_two, art_three = find_stories('TSLA')

move_percent = find_move_percent(days_price, difference, direction)

message = MIMEMultipart()
message['From'] = gmail
message['To'] = 'loadedcoal@gmail.com'
message['Subject'] = f'{STOCK} is {move_percent} today!'

body = f'Subject: {STOCK} is {move_percent} today\n\nHello,\n{STOCK} is {move_percent} today! Here are the latest stories:\n\n{art_one}\n{art_two}\n{art_three}'
message.attach(MIMEText(body, 'plain', 'utf-8'))

connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()
connection.login(user=gmail, password=gmail_api_key)
connection.sendmail(gmail, 'loadedcoal@gmail.com', message.as_string())

print('Your email was sent!')




