# security_news_scraper

**app.py**: calls others.py and twitter.py functions and save data to database

**web.py**: web app to display data 

**others.py**: collect news from https://thehackernews.com/ , https://www.exploit-db.com/ 

**twitter.py**: collect news from specified accounts 

**config.py**: required keys to collect data from twitter (You should contact twitter to get the keys) 

**db.py**: manage database queries

# Install steps (python3.9):
  ~$ pip install -r requirements.txt
  
  ~$ python web.py 

  Install mongodb : Follow steps on https://docs.mongodb.com/manual/administration/install-community/
  
  ~# service mongod start

### Create cron job to run app.py periodically

Example every 1h :

~$ crontab -e

then add this line (Change /path/to/file according to your environment) 

\* \* \* \* \* /usr/bin/python /path/to/file/app.py

# Suggestions
Project is still under development so if you have any suggestions please let me know :)
