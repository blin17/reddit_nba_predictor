# NBA Subreddit Front Page Predictor
Multinomial Naive Bayes model that predicts the score bucket of a post based on it's title, time of posting, url, and contents. The model achieves 75% accuracy of predicting within 1 score bucket of the actual post, which matches the baseline model.

Baseline Model: Softmax Regression which predicts the score bucket of a post based on it's number of comments (2 Output values).


# Scraper

File: 
/scripts/archive_scraper.py

Command:
run python archive_scraper.py -d 2016 6 0 -s nba

Note: I recommend using Archive Scraper. It allows you create backlogs of data. Lazy Scraper is just for daily scrapping reddit.

# Analysis 
r_nba-[Analysis] contains the code for feature analysis to determine which ones are important and creating a baseline model for predicting front page based on the number of commands.

r_nba-[Model] contains the code on predicting front page based on different attributes