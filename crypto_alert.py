# import the required libraries

import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import yagmail
import coinmarketcapapi
from pretty_html_table import build_table
import vonage

# load environmental variables
load_dotenv()

MY_TOKEN = os.getenv("MY_TOKEN")
API_KEY = os.getenv('COIN_API_KEY')
RECIPENT_EMAIL = os.getenv("RECIPENT_EMAIL")
MAIL_FROM_PASS = os.getenv("MESSAGE_FROM_PASS")
KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMS_TO = os.getenv("TO_SMS")

# instantiate the CMC api
cmc = coinmarketcapapi.CoinMarketCapAPI(API_KEY)

# setting up client for VONAGE TEXT messages
client = vonage.Client(key=KEY, secret=SECRET)
sms = vonage.Sms(client)

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


# send updates via telegram
def send_telegram(message):
    requests.post(
        'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown'.format(MY_TOKEN, 786259592, message))


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
    

def bear_market():
    # returns true if bear market (btc/eth down 15% or more in 24hr or 20% or more last 7 days)
    return (btc_change_24_hr <= -15 or eth_change_24_hr <= -15) or (btc_change_7days <= -20 or eth_change_7days <= -20)
def bull_market():
    # returns true if bull market (btc/eth up 15% or more in 24hr or 20% or more last 7 days)
    return (btc_change_24_hr >= 15 or eth_change_24_hr >= 15) or (btc_change_7days >= 20 or eth_change_7days >= 20)


btc = cmc.cryptocurrency_quotes_latest(symbol='BTC', convert='USD')
eth = cmc.cryptocurrency_quotes_latest(symbol='ETH', convert='USD')
btc_change_7days = btc.data['BTC']['quote']['USD']['percent_change_7d']
btc_change_24_hr =  btc.data['BTC']['quote']['USD']['percent_change_24h']
eth_change_7days = eth.data['ETH']['quote']['USD']['percent_change_7d']
eth_change_24_hr = eth.data['ETH']['quote']['USD']['percent_change_24h']

if __name__ == "__main__":

    print('Sending Email')
    send_emails(get_apes_trend())
    print('Email Sent')

    if bear_market():
        send_telegram('Seems Like We Are Entering a Bear Market.\n Buy the Fucking Dip')
        responseData = sms.send_message({
        "from": "Bully",
        "to": SMS_TO,
        "text": "Buy The Fucking Dip!!!",})

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        print('sent bear market notification')

    elif bull_market():
        send_telegram('Bull Market Happening baby!!!')
        responseData = sms.send_message({
        "from": "Bully",
        "to": SMS_TO,
        "text": "Bull Market Baby!!!",})

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        print('sent bull market notification')

    print('No bear or bull Market')

print('Done for the day', str(datetime.now()))