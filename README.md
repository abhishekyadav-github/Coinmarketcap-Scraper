# Coinmarketcap-Scraper
Scrape data from coinmarketcap.com and send it to a Django BE using HTTP POST request every 5sec which will either create or update the coin data. And have a FE using Reactjs which will fetch data from BE every 3sec and show that data in tabular format.

***
To run the code do the following:

Step1: From root dir run scraper.py using 'python scraper.py' command in a separate terminal. 

Step2: Go to dir crypto_project using 'cd crypto_project' command and run the django server using './manage.py runserver' comamnd in a separate terminal.

Step3: Go to dir client/crypto_app_fe and run FE using 'npm start' command in a separate terminal.
***

You will be redirected to localhost:3000 where you will see Crypto Coins data getting updated every 3 secs.
To check the BE data you can got to localhost:8000/admin, but before that you'll have to create a superuser using './manage.py createsuperuser' and use these credentials to login to admin panel of django.

HAPPY SCRAPING!!
