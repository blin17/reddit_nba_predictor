"""
Reddit scraper that scrapes last 1000 posts from the nba subreddit
Author: @Brian Lin 
"""


import praw
import csv
import datetime

# Script Parameters
subreddit = 'nba'
post_limit = 1000 	# how many posts we want to scrape
cache_limit = 50 	# after how many posts do we save cache to csv
today = datetime.date.today()
file_dir = "../data"
file_name = "{0}-{1}-{2}_post_data.csv".format(today.year,today.month,today.day) # output file name

# User Agent allows the reddit API to identify the script
# Format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = "python:r_nba_app:v1 (by /u/fugitivedenim)"

r = praw.Reddit(user_agent=user_agent)
posts = r.get_subreddit(subreddit).get_hot(limit = post_limit)

post_cache = []
columns = ['id','title', 'url', 'domain', 'permalink', 'subreddit','score', 'num_comments', 
		'num_duplicates', 'gilded', 'created', 'author_flair_text', 'author',
		'is_self', 'over_18']

csv_file = open(file_dir + "/" + file_name,"wb+")
writer = csv.writer(csv_file)
writer.writerow(columns)

def clear_cache():
	for p in post_cache:
		try:
			l = []
			for c in columns:
				if c == 'num_duplicates':
					l.append(p[1])
				elif c == 'title':
					l.append(getattr(p[0],c).encode('utf8'))
				else:
					l.append(getattr(p[0],c))
			writer.writerow(l)
		except Exception as e:
			print e
			print [getattr(p[0],c) if c != 'num_duplicates' else p[1] for c in columns]
			pass

counter = 1
for post in posts:
	print "{0}/{1} Posts".format(counter,post_limit)
	counter +=1
	#num_dupes
	duplicates = post.get_duplicates()
	num_dupes = 0
	d_cache = []
	for d in duplicates:
		d_cache.append(d)
		num_dupes +=1
	post_cache.append((post,num_dupes))
	post_cache.extend([(d,num_dupes)for d in d_cache])
	if len(post_cache) > cache_limit:
		clear_cache()
		post_cache = []

clear_cache()
