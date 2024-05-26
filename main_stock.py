import pprint
import requests
import os
from dotenv import load_dotenv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

AV_url = os.getenv('alpha_vantage_url')
AV_api_key = os.getenv('alphaV_api_key_second')

NAPI_url = os.getenv('newsapi_url')
NAPI_api_key = os.getenv('newsapi_key')

gmail = os.getenv('burner_gmail')
gmail_api_key = os.getenv('gmail_app_pass')

STOCK = "NVDA"
COMPANY_NAME = "NVIDIA"
TARGET_EMAIL = os.getenv('target_email')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"

today = datetime.date.today()
old = today - datetime.timedelta(days=10)


# Function to call the API and get data to work with
def call_stock_api(stock, api_key, endpoint):
    stock_params = {
        'function': 'Time_Series_Daily',
        'symbol': stock,
        'apikey': api_key,

    }

    stock_call = requests.get(endpoint, params=stock_params)
    stock_call.raise_for_status()
    datas = stock_call.json()['Time Series (Daily)']
    datas_list = [value for (key, value) in datas.items()]
    yesterday_data = datas_list[0]
    yesterday_data_plus = datas_list[1]

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


# Function to check percentage of move and return with a unicode arrow
def find_move_percent(day, difference, direction):
    if difference == 'stable' and direction == 'stable':
        return 'stable'

    percentage = (int(difference) / int(day)) * 100

    if direction == 'up':
        arrow = '\u2191'
    else:
        arrow = '\u2193'

    return f'{arrow} {percentage}%'


price_yesterday, price_day_before = call_stock_api(STOCK, AV_api_key, STOCK_ENDPOINT)

days_price, difference, direction = find_sufficient_movements(price_yesterday, price_day_before)


# Function that searches News API for relevant stories, the free API used in this project is not the most effective.
# If your planning on searching for big companies like google, tesla or microsoft you will get relevant articles.
def find_stories(stock):
    news_params = {
        'q': stock,
        'pageSize': 3,
        'sortBy': 'popularity',
        'apikey': NAPI_api_key
    }

    grab_news = requests.get(NEWS_ENDPOINT, params=news_params)
    grab_news.raise_for_status()
    dataN = grab_news.json()

    article_list = []

    for each in dataN['articles'][:3]:
        if each is None:
            article_list.append('Story not available')
        else:
            article_list.append(f'Title: {each['title']}\nSource: {each['source']['name']}\nLink: {each['url']}\n')

    article_one, article_two, article_three = (article_list + ['Story not available'] * 3)[:3]

    return article_one, article_two, article_three


art_one, art_two, art_three = find_stories(COMPANY_NAME)

move_percent = find_move_percent(days_price, difference, direction)

# Finally we take the relevant information and compile it in to an email and send it.
# I will be testing this in python anywhere for a while with different companies just for the hell of it, I may or may
# not tweek the code. This was a project I worked on and I was able to make it run on my own with only the endpoint
# documentation so for the most part I am satisfied with the outcome, I also really don't plan on using it.

message = MIMEMultipart()
message['From'] = gmail
message['To'] = TARGET_EMAIL
message['Subject'] = f'{STOCK} is {move_percent} today!'

body = f'Subject: {STOCK} is {move_percent} today\n\nHello,\n{STOCK} is {move_percent} today! Here are the latest stories:\n\n{art_one}\n{art_two}\n{art_three}'
message.attach(MIMEText(body, 'plain', 'utf-8'))

connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()
connection.login(user=gmail, password=gmail_api_key)
connection.sendmail(gmail, 'loadedcoal@gmail.com', message.as_string())

print('Your email was sent!')
