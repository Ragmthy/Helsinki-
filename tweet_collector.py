# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 12:48:17 2018

@author: Ragini
"""
import tweepy
import pandas as pd
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#imports in API credentials into here
import twitter_credentials_program

 #https://github.com/tweepy/tweepy
import csv

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(twitter_credentials_program.CONSUMER_KEY, twitter_credentials_program.CONSUMER_SECRET)
	auth.set_access_token(twitter_credentials_program.ACCESS_TOKEN, twitter_credentials_program.ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	df = pd.DataFrame(outtweets, columns=["id","created_at","text"])
	df.to_csv("{}_tweets.csv".format(screen_name))
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
   user_input = input("Enter the Twitter username you wanna see tweets of: \n")
    #In this Hackathon, we chose to analyze Trump's tweets: so insert the username @realDonaldTrump
   get_all_tweets(user_input)