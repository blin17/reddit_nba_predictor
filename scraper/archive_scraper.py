"""
Reddit nba Archive scraper for getting around impose 1000 limit
Author: @Brian Lin
"""
import praw
import datetime
import time
import pprint
import csv
from sys import argv

'''
run python archive_scraper.py -d 2016 6 0 -s nba
'''
user_agent = "python:r_nba_app:v1 (by /u/fugitivedenim)"
today = datetime.datetime.today()
default_date = {'year':today.year, 'month':today.month,'day':today.day}
default_num_windows = (14*5*4) #14 per week, default is 3 months
default_window_length = 12
cache_limit = 50
post_limit = 100
file_dir = '../data/backlog'
relevant_columns = ['id','title', 'url', 'domain', 'permalink', 'subreddit','score', 'num_comments', 
			'gilded', 'created', 'author_flair_text', 'author', 'is_self', 'over_18']

def query_generator(start_date,end_date):
	''' query_generator() creates inputs for the praw search field. 
		Note: start_date must be before end_date
	'''
	utc1 = int(time.mktime(start_date.timetuple()))
	utc2 = int(time.mktime(end_date.timetuple()))
	url = 'https://www.reddit.com/r/nba/search?'
	params = {'q':('timestamp:{0}..{1}'.format(utc1, utc2)), 'restrict_sr':'on','syntax':'cloudsearch'}
	return url,params


def generate_file_name(date1,date2,subreddit):
	s = 'all' if subreddit is None else subreddit
	utc1 = int(time.mktime(date1.timetuple()))
	utc2 = int(time.mktime(date2.timetuple()))
	return ('{0}-{1}-{2}-{3}_to_{4}-{5}-{6}-{7}_{8}_data.csv'
				.format(date1.year,date1.month,date1.day,utc1
					,date2.year,date2.month,date2.day,utc2,s))


def handle_posts(posts, file_name, iteration,num_windows):
	'''	handle_posts() takes an array of posts and saves them into a file 
		every time the cache array hits the cache limit
	'''
	def clear_cache(writer, post_cache):
		for p in post_cache:
			try:
				l = []
				for c in relevant_columns:
					if c == 'title':
						l.append(getattr(p,c).encode('utf8'))
					else:
						l.append(getattr(p,c))
				writer.writerow(l)
			except Exception as e:
				print e
				print [getattr(p,c) for c in relevant_columns]
		return 
	
	post_cache = []
	csv_file = open(file_dir + "/" + file_name,"wb+")
	writer = csv.writer(csv_file)
	writer.writerow(relevant_columns)
	num_posts = 0
	for post in posts: 
		num_posts +=1
		post_cache.append(post)
		if len(post_cache) > cache_limit:
			clear_cache(writer,post_cache)
			post_cache = []
	clear_cache(writer,post_cache)
	print 'iteration: {0}/{1} file: {2} num_posts: {3}'.format(iteration+1, num_windows, file_name, num_posts)
	return


def main(params):
	''' main() takes in a few parameters:
			date: the inital date that we are scrape from
			window_length: the duration between the start and end date
			num_windows: the number of windows we want to scrape
			subreddit: subreddit we want to scrape from; default None
		Note: if you need to debug, run pprint with vars(posts)
	'''
	window_length = params['window_length'] if 'window_length' in params else default_window_length
	subreddit = params['subreddit'] if 'subreddit' in params else None
	date = params['date'] if 'date' in params else default_date
	num_windows = params['num_windows'] if 'num_windows' in params else default_num_windows

	initial_date = datetime.datetime(**date)
	time_diff = datetime.timedelta(hours=window_length)
	date1 = initial_date
	date2 = initial_date
	for i in range(num_windows):
		date1 = date2
		date2 = date1+time_diff
		r = praw.Reddit(user_agent=user_agent)
		if subreddit is not None:
			r = r.get_subreddit(subreddit)
		query = query_generator(date1, date2)
		file_name = generate_file_name(date1,date2, subreddit)
		query[1]['limit'] = 100
		posts = r.search("", params=query[1])
		handle_posts(posts, file_name, i, num_windows)
	
if __name__ == "__main__":
	''' commands:
		-d: "-d yyyy mm dd" refers to date of initial submission
		-s: "-s subreddit" refers to the subreddit used for scraping (Leave empty for none)
		-w: "-w window_length" refers to scraping windows. this depends on how popular the subreddit is
	'''
	params = {}
	if len(argv) > 1:
		args = filter(None," ".join(argv[1:]).split("-"))
		for arg in args:
			command = arg.split()
			if command[0] == 'd':
				date = {}
				date['year'] = int(command[1])
				date['month'] = int(command[2])
				date['day'] = int(command[3])
				params['date'] = date
			elif command[0] == 's':
				params['subreddit'] = command[1]
			elif command[0] == 'w':
				params['window_length'] = int(command[1])
			elif command[0] == 'n':
				params['num_windows'] = int(command[1])
	main(params)
	

