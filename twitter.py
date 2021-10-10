import requests
from config import *
from datetime import datetime
from db import database

db = database()

def get_user_id(username):
	headers = {
	    'Authorization': 'Bearer {}'.format(TOKEN),
	}

	params = (
	    ('usernames', username),
	)

	response = requests.get('https://api.twitter.com/2/users/by', headers=headers, params=params)

	try:
		return response.json()['data'][0]['id']
	except:
		return response.json()['errors'][0]['detail']


def get_tweets(user_id,username):
	headers = {
	    'Authorization': 'Bearer {}'.format(TOKEN),
	}
	response = requests.get('https://api.twitter.com/2/users/{}/tweets'.format(user_id), headers=headers)
	data = response.json()['data']
	for i in range(len(data)):
		data[i]['type'] = "tweet"
		data[i]['date'] = str(datetime.now())
		data[i]['link'] = "https://twitter.com/{}/status/{}".format(username,data[i]['id'])
		data[i].pop('id')
		data[i]['source']='twitter'
		data[i]['score']=0
		data[i]['show']=1
	return data

def add_user(username):
	user_id = get_user_id(username)
	key={"user_id":user_id,'show':1}
	print(db.find("twitter_users",key).count())
	if db.find("twitter_users",key).count()>0:
		return False
	u = {'user_id':user_id,'username':username,'muted':0,'show':1}
	db.update(u,u,'twitter_users')
	return True

def del_user(username):
	user_id = get_user_id(username)
	u = {'user_id':user_id,'username':username}
	return db.update(u,{"$set":{'show':0}},'twitter_users')

add_user("MITREattack")