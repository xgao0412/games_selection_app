from flask import Flask, render_template,redirect,url_for,request
import twitterscraper
from twitterscraper import query_tweets
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

@app.route('/')
def student():
	return render_template('student.html')

@app.route('/result',methods=['POST','GET'])
def result():

	if request.method =='POST':
		app_name = request.form['Name']

	def get_tweet(app):
		return query_tweets(app, limit=None,
							begindate=dt.date.today()-dt.timedelta(days=1), 
							enddate=dt.date.today(), 
							poolsize=20, 
							lang='en'
							)
	
	tweet = get_tweet(app=app_name)

	length = len(tweet)
	likes= 0
	reply= 0
	retweets= 0
	text=[]    
	if tweet:

	    length = len(tweet)
	    likes= 0
	    reply= 0
	    retweets= 0
	    text = []
	        
	for line in tweet:
	    likes+=int(line.likes)
	    reply+=int(line.replies)
	    retweets+=int(line.retweets)

	    if line.text:
	        text.append(line.text)

	analyzer = SentimentIntensityAnalyzer()
	pos=[]
	for i in text:
	    output = analyzer.polarity_scores(i)
	    pos.append(output['pos'])
	pos_value = [a for a in pos if a>0]

	dic = {'tweets':length,'likes':likes,'reply':reply,'retweets':retweets,'positive sentiment':len(pos_value)}


	return render_template('index.html',result = dic)





if __name__ == '__main__':
	app.run(debug=True)