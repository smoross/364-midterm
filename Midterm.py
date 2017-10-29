from flask import Flask, request, render_template, make_response
import json
import requests
import os

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import twitter
import tweepy
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'

consumer_key='E8kcyPIeEDFRYzuWs0BvSLOp6'
consumer_secret='0FKDIWo1Iw519iRW9aZhsg3ZKqausogzAL1RFpoo2AuH9trraS'
access_token='290741488-pE5Hm42EDYVpTy2XwFPOj5MGjCCqsZl7xWENMwop'
access_token_secret='uwSYdQlH192ilNmtNmPoDPiuG51I67oXHtdivLDY9F6ga'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class TwitterForm(FlaskForm):
    keyword = StringField('Insert a keyword', validators=[ Required() ])
    submit = SubmitField('Submit')

@app.route('/')
def hello_user():
	response = make_response("Hello Tweeter! <img src='/static/twitter-2012-positive-logo-916EDF1309-seeklogo.com.png'/>")
	response.set_cookie('cookie_name',value='values')
	return response

@app.route('/index')
def home_route():
	Form = TwitterForm()
	return render_template('twitter-form.html', form=Form)

@app.route('/result', methods= ['POST'])
def result():
	form = TwitterForm(request.form)
	if request.method == 'POST':
		keyword = form.keyword.data
		print (keyword)
		x = tweepy.Cursor(api.search, q=keyword, result_type="recent", include_entities=True, lang="en", show_user=True).items(10)
		accum = []
		for tweet in x:
			accum.append(tweet.text)
			print (tweet)
		return render_template('result.html', tweets=accum)

@app.route('/twitter-info/<username>')
def user(username):
	tweets_for_user = api.user_timeline(username)
	accum = []
	for tweet in tweets_for_user:
		accum.append(tweet.text)
	
	return render_template('tweets_for_user.html', tweets=accum, user=username)

@app.route('/follower-info/<username>')
def followers(username):
	twitter_user = api.followers(username)
	accum = []
	for tweet in twitter_user:
		accum.append(tweet.name)		
	return render_template('followers.html', tweets=accum, user=username)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def page_error(e):
    return render_template('500.html')

if __name__=='__main__':
	app.run(debug=True)
