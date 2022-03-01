import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import yagmail
from pretty_html_table import build_table
import vonage
from requests.sessions import Session


load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")
RECIPENT_EMAIL = os.getenv("RECIPENT_EMAIL")
MAIL_FROM_PASS = os.getenv("MESSAGE_FROM_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMS_TO = os.getenv("TO_SMS")
API_KEY = os.getenv('COIN_API_KEY')


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5'


def bear_market():
    # returns true if bear market (btc/eth down 10% or more in 24hr or 20% or more last 7 days)
    data = json.loads(session.get(url).text)
    btc_change_24_hr = data['data'][0]['quote']['USD']['percent_change_24h']
    btc_change_7days = data['data'][0]['quote']['USD']['percent_change_7d']
    eth_change_7days = data['data'][1]['quote']['USD']['percent_change_24h']
    eth_change_24_hr = data['data'][1]['quote']['USD']['percent_change_7d']
    return (btc_change_24_hr <= -10 or eth_change_24_hr <= -10) or (btc_change_7days <= -20 or eth_change_7days <= -20)


def bull_market():
    # returns true if bull market (btc/eth up 10% or more in 24hr or 20% or more last 7 days)
    data = json.loads(session.get(url).text)
    btc_change_24_hr = data['data'][0]['quote']['USD']['percent_change_24h']
    btc_change_7days = data['data'][0]['quote']['USD']['percent_change_7d']
    eth_change_7days = data['data'][1]['quote']['USD']['percent_change_7d']
    eth_change_24_hr = data['data'][1]['quote']['USD']['percent_change_24h']
    return (btc_change_24_hr >= 10 or eth_change_24_hr >= 10) or (btc_change_7days >= 20 or eth_change_7days >= 20)

def get_apes_trend():
    apes_wisdom = 'https://apewisdom.io/api/v1.0/filter/all-crypto'
    response = requests.get(apes_wisdom).text
    result = json.loads(response)
    Ranks, Tickers, Names, Mentions, Upvotes = [], [], [], [], []
    for i in range(10):
        # get the top 10 TRENDING COINS
        Ranks.append(result['results'][i]['rank'])
        Tickers.append(result['results'][i]['ticker'])
        Names.append(result['results'][i]['name'])
        Mentions.append(result['results'][i]['mentions'])
        Upvotes.append(result['results'][i]['upvotes'])

    df = pd.DataFrame({
        "Ranks": Ranks,
        "Tickers": Tickers,
        "Names": Names,
        "Mentions": Mentions,
        'Upvotes': Upvotes}, index=Ranks)

    result_prettified = build_table(df, 'blue_light')
    return result_prettified



def send_telegram(message):
    requests.post(
        'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown'.format(MY_TOKEN, 786259592, message))

# function to send emails
def send_emails(contents):
    global RECIPENT_EMAIL
    recipent_email_address = RECIPENT_EMAIL
    global MAIL_FROM_PASS
    password1 = MAIL_FROM_PASS
    msg_from = EMAIL_FROM
    yag = yagmail.SMTP(msg_from, password1)
    content = ["<h1> TODAY'S TREND... </h1>", contents + '<h1> End Of Message </h1>']
    yag.send(to=recipent_email_address, subject= '[Automated Email] Apes Trend: ' + 
    str(datetime.now().date()), contents=content)