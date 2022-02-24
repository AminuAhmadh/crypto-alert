# CRYPTO_ALERT: Dip, Surge and Trend

This app will notify you of bitcoin or ethereum massive drop or gain via Text message and telegram. It would also sends you the top ten coins trending on https://Apewisdom.io 

This project isn't done yet. It's a work in progress. will continue updating. Please let me know a specific feature you'll want me to add or if you find any issue with the code.


## First

The `requirements.txt` file should list all Python libraries that the script depend on, and you should install it using:

""" pip install -r requirements.txt """


## Second

You have to register an account with vonage to get access to their SMS API. So head over to https://dashboard.nexmo.com/ to register and account and collect your KEY and SECRET for client authentication.
Secondly, head over to https://api.coinmarketcap.com to get your free API key for crypto data inquiry.

## Third

An Email plus password is required by the library `yagmail` to send yourself Email. You can create a new gmail just for that purpose or use your own. And for it to work, you have to turn on Less secure app on https://accounts.google.com for that account that you'll use to send yourself email.

## Fourth

You have to create a bot on telegram using @BotFather or use one if you already have it. That bot will be used to send yourself message on telegram.

## Lastly

You should put all your credentials (APIs, Secret keys, email and pass) into `.env` file and access them using enviromental variable so that nobody can have access to your credentials.

## Finally

The last thing you want to do is to Automate this task (locally or preferrebly on the cloud) so that it runs daily or weekly or any how you want. 

## Happy Coding...