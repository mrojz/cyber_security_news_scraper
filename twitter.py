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

def jsonify_tweets(data,username):
	for i in range(len(data)):
		data[i]['type'] = "tweet"
		data[i]['date'] = data[i]['created_at'].replace('T',' ').replace('Z','').split('.')[0]
		data[i].pop('created_at')
		data[i]['link'] = "https://twitter.com/{}/status/{}".format(username,data[i]['id'])
		data[i].pop('id')
		data[i]['source']='twitter'
		data[i]['score']=0
		data[i]['show']=1
	return data

def get_tweets(user_id,username):
	headers = {
	    'Authorization': 'Bearer {}'.format(TOKEN),
	}
	response = requests.get('https://api.twitter.com/2/users/{}/tweets?max_results=100&tweet.fields=created_at'.format(user_id), headers=headers)
	data = jsonify_tweets(response.json()['data'],username)
	return data