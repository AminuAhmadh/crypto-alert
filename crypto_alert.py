# import the required libraries
from datetime import datetime
from time import time
import vonage
import os
import time
from utils import get_apes_trend
from utils import bear_market, bull_market
from utils import send_emails, send_telegram

KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")
API_KEY = os.getenv('COIN_API_KEY')
SMS_TO = os.getenv("TO_SMS")

# setting up client for VONAGE TEXT messages
client = vonage.Client(key=KEY, secret=SECRET)
sms = vonage.Sms(client)

while True:
    print('Sending Email')
    send_emails(get_apes_trend())
    print('Email Sent')

    if bear_market():
        send_telegram('Seems Like We Are Entering a Bear Market.\nBuy the Fucking Dip')
        responseData = sms.send_message({
        "from": "NEON",
        "to": SMS_TO,
        "text": "Buy The Fucking Dip!!!",})

        if responseData["messages"][0]["status"] == "0":
            print("SMS sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        print('sent bear market notification')

    elif bull_market():
        send_telegram('Bull Market Happening baby!!!')
        responseData = sms.send_message({
        "from": "NEON",
        "to": SMS_TO,
        "text": "To The Fucking Moon!!!",})

        if responseData["messages"][0]["status"] == "0":
            print("SMS sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        print('sent bull market notification')
    else:
        print('No bear or bull Market')
    
    print('Done for the day', str(datetime.now()))
    # wait 24 hours
    time.sleep(86400)
