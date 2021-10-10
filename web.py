from flask import Flask ,Response, render_template , request , session, redirect, url_for , send_file , flash
from db import database
from gevent import monkey
from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
from bson.objectid import ObjectId
from twitter import get_user_id

app = Flask(__name__)

db=database()

app.secret_key = b'_5#y2L"F4Q8zkaqsda5esdlzfkaz5"]/'

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.args.get("filter")!=None and request.args.get("date")!=None and request.args.get("score")!=None:
		f = {'type':request.args.get("filter"),'show':1}
		news = db.find("news",f).sort('date',int(request.args.get('date'))).sort('score',int(request.args.get('score')))

	elif request.args.get("filter")!=None and request.args.get("date")!=None:
		f = {'type':request.args.get("filter"),'show':1}
		news = db.find("news",f).sort('date',int(request.args.get('date')))

	elif request.args.get("filter")!=None and request.args.get("score")!=None:
		f = {'type':request.args.get("filter"),'show':1}
		news = db.find("news",f).sort('score',int(request.args.get('score')))

	elif request.args.get("score")!=None and request.args.get("date")!=None:
		news = db.find("news",{'show':1}).sort('date',int(request.args.get('date'))).sort('score',int(request.args.get('score')))

	elif request.args.get("score")!=None:
		news = db.find("news",{'show':1}).sort('score',int(request.args.get('score')))

	elif request.args.get("date")!=None:
		news = db.find("news",{'show':1}).sort('date',int(request.args.get('date')))

	elif request.args.get("filter")!=None:
		f = {'type':request.args.get("filter"),'show':1}
		news = db.find("news",f)
	else:
		news = db.find("news",{'show':1})
	return render_template('index.html',news=news)


@app.route('/news/<news_id>', methods=['GET', 'POST'])
def news(news_id):
	news = db.find("news",{"_id":ObjectId(news_id)})
	for n in news:
		new=n
	return render_template('news.html',new=new)

@app.route('/news/delete/<news_id>', methods=['GET', 'POST'])
def delete_news(news_id):
	news = db.update({"_id":ObjectId(news_id)},{"$set":{'show':0}},'news')
	return redirect(url_for('index'))

@app.route('/news/upvote/<news_id>', methods=['GET', 'POST'])
def upvote_news(news_id):
	x = request.args.get('vote')
	news = db.update({"_id":ObjectId(news_id)},{"$inc": {'score': int(x)}},'news')
	return redirect(url_for('index'))


@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
	twitters = db.find('twitter_users',{'show':1})
	return render_template('twitter.html',twitters=twitters)


@app.route('/birds/mute/<bird_id>', methods=['GET', 'POST'])
def mute_bird(bird_id):
	x = request.args.get('mute')
	bird = db.update({"_id":ObjectId(bird_id)},{"$set":{'muted':int(x)}},'twitter_users')
	return redirect(url_for('index'))

@app.route('/birds/delete/<bird_id>', methods=['GET', 'POST'])
def delete_bird(bird_id):
	bird = db.update({"_id":ObjectId(bird_id)},{"$set":{'show':0}},'twitter_users')
	return redirect(url_for('index'))

@app.route('/birds/add/<bird_name>', methods=['GET', 'POST'])
def add_user(bird_name):
	user_id = get_user_id(bird_name)
	key={"user_id":user_id,'show':1}
	if db.find("twitter_users",key).count()>0:
		return False
	u = {'user_id':user_id,'username':bird_name,'muted':0,'show':1}
	db.update(u,u,'twitter_users')
	return redirect(url_for('twitter'))
if __name__ == "__main__":
	monkey.patch_all(ssl=False)
	http_server = WSGIServer(('0.0.0.0', 5000), DebuggedApplication(app))
	http_server.serve_forever()