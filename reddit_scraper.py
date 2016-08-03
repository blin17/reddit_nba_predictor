import praw
import datetime
import pprint


# User Agent allows the reddit API to identify the script
# <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = "python:r_nba_app:v1 (by /u/fugitivedenim)"

r = praw.Reddit(user_agent=user_agent)
posts = r.get_subreddit('nba').get_hot(limit = 10)

'''
Post Table
	----observed attributes---
	id PRIMARY KEY INTEGER 
	title TEXT
	url	TEXT
	url_domain TEXT
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


	post_object = {
		'title' : '',
		'url' : '',
		'url_domain' : '',
		'permalink' : '',
		'score' : 0,
		'num_comments' : 0,
		'num_duplicates' : 0,
		'time_created' : 0,
		'author_flair_text' : '',
		'author' : '',
		'gilded' : 0,
		'is_self' : 0,
		'over_18' : 0
	}
'''


id = 0
post_table = []

#<class 'praw.objects.Submission'>
for post in posts:
	id += 1
	post_object = {
		'id': id,
		'title' : post.title,
		'url' : post.url,
		'url_domain' : post.domain,
		'permalink' : post.permalink,
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

pprint.pprint(post_table)


#pprint.pprint(karma_by_subreddit)