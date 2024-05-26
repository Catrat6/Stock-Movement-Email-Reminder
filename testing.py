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

NAPI_api_key = os.getenv('newsapi_key')

NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"

news_params = {
        'q': 'Tesla',
        'pageSize': 10,
        'sortBy': 'popularity',
        'apikey': NAPI_api_key
}

data = requests.get(NEWS_ENDPOINT, params=news_params)
data.raise_for_status()
x = data.json()

art_list = []

for each in x['articles'][:3]:
        art_list.append(f'Title: {each['title']}\nSource: {each['source']['name']}\nLink: {each['url']}\n')

article_one, article_two, article_three = (art_list + [None] * 3)[:3]

print(article_one, article_two, article_three)

