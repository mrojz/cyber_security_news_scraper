import requests, re
from time import sleep
from datetime import datetime
from db import database
from twitter import *
from others import *


db=database()

#Grab from hacker news
for url in urls:
    r = get_hacker_news(url)
    for i in r:
        key={ "link":i["link"] }
        if db.find("news",key).count()>0:
            continue
        db.update(key,i,"news")

#Grab from exploitdb
r = get_exploitdb()
for i in r:
    key={"link":i["link"]}
    if db.find("news",key).count()>0:
        continue
    db.update(key,i,"news")

#Grab from users
twitter_users = db.find("twitter_users",{'muted': 0,'show':1})
for user in twitter_users:
    tweets = get_tweets(user['user_id'],user['username'])
    for tweet in tweets:
        key = {'link':tweet['link']}
        if db.find("news",key).count()>0:
            continue
        db.update(key,tweet,"news")

