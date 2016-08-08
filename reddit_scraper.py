'''
Reddit /r/nba Scraper - Scrapes reddit posts

# Data Schema for the Post Table
Post Table
	----observed attributes---
	id PRIMARY KEY INTEGER 
	title TEXT
	url	TEXT
	url_domain TEXT
	subreddit TEXT
	permalink TEXT
	score INTEGER 
	num_comments INTEGER
	num_duplicates INTEGER
	time_created DATETIME
	author_flair_text TEXT
	author TEXT
	gilded INTEGER
	is_self INTEGER // BOOLEAN
	over_18 INTEGER // BOOLEAN
'''

import praw
import datetime
import csv
import json
import pprint

post_limit = 10
clear_cache_limit = 1

# User Agent allows the reddit API to identify the script
# Format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = "python:r_nba_app:v1 (by /u/fugitivedenim)"

r = praw.Reddit(user_agent=user_agent)
posts = r.get_subreddit('nba').get_hot(limit = post_limit)


id = 0
post_table = []


csv = csv.writer(open("posts_data.csv", "wb+"))
columns = ['id','title', 'url', 'url_domain', 'permalink', 'subreddit','score', 'num_comments', 
		'num_duplicates', 'gilded', 'time_created', 'author_flair_text', 'author',
		'is_self', 'over_18']
csv.writerow(columns)

def clear_posts():
	global post_table
	for p in post_table:
		try:
			csv.writerow([p['id'],p['title'].encode('utf8'), p['url'].encode('utf8'), p['url_domain'].encode('utf8'), p['permalink'].encode('utf8'), p['subreddit'], p['score'], p['num_comments'], p['num_duplicates'], p['gilded'], p['time_created'], p['author_flair_text'], p['author'], p['is_self'], p['over_18']])
			for c in columns:

		except Exception as e:
			# Used to catch bad characters that break the csvwrite
			print e
			pass
	post_table = []

for post in posts: 
	id += 1
	print str(id) + " " + post.title
	post_object = {
		'id': id,
		'title' : post.title,
		'url' : post.url,
		'url_domain' : post.domain,
		'permalink' : post.permalink,
		'subreddit' : post.subreddit,
		'score' : post.score,
		'num_comments' : post.num_comments,
		'num_duplicates' : 0,
		'time_created' : post.created,
		'author_flair_text' : post.author_flair_text,
		'author' : post.author,
		'gilded' : post.gilded,
		'is_self' : 1 if post.is_self == 'True' else 0,
		'over_18' : 1 if post.over_18 == 'True' else 0
	}
	# Gets all duplicates of the same link (most are in other subreddits)
	duplicates = post.get_duplicates()
	num_dupes = 0
	dupes = []
	for dupe in duplicates:
		id += 1
		num_dupes +=1
		dupe_object = {
			'id' : id,
			'title' : dupe.title,
			'url' : dupe.url,
			'url_domain' : dupe.domain,
			'permalink' : dupe.permalink,
			'subreddit' : dupe.subreddit,
			'score' : dupe.score,
			'num_comments' : dupe.num_comments,
			'num_duplicates' : 0,
			'time_created' : dupe.created,
			'author_flair_text' : dupe.author_flair_text,
			'author' : dupe.author,
			'gilded' : dupe.gilded,
			'is_self' : 1 if dupe.is_self == 'True' else 0,
			'over_18' : 1 if dupe.over_18 == 'True' else 0
		}
		dupes.append(dupe_object)

	post_object['num_duplicates'] = num_dupes
	post_table.append(post_object)

	for item in dupes:
		item['num_duplicates'] = num_dupes
		post_table.append(item)
	if id % clear_cache_limit == 0:
		clear_posts()
clear_posts()
