'''
Bunch of Functions that help with Naive Bayes
@author: Brian Lin

'''

import pandas as pd
import numpy as np

common_words = pd.read_csv('../lib/common_words.txt', header = None)[0].values

def remove_common_words(title, common_words):
# removes common words from a string and then splits them
    tw = map(lambda d: d.strip(".,:()[]!?\"").lower(),title.split())
    return [w for w in tw if w not in common_words]

def generate_words_and_scores(titles, scores):
# Takes in Series of Titles and Scores, Returns a Dataframe with words and scores
    title_words = []
    score_words = []
    for index in range(len(titles)):
        title_word_list = remove_common_words(titles.iloc[index], common_words)
        title_words.extend(title_word_list)
        score_words.extend([scores.iloc[index]] * len(title_word_list))
    title_words_s = pd.Series(title_words)
    words_scores_df = pd.concat([title_words_s, pd.Series(score_words)], axis = 1)
    words_scores_df.columns = ['word', 'score']
    return words_scores_df

def sanitize_and_split_titles(title_s):
    l = []
    for title in title_s:
        title_r = remove_common_words(title, common_words)
        l.append(title_r)
    return l

def create_feature_row(title, word_vec):
    feature_row = np.zeros((len(word_vec),))
    for word in title:
        if word in word_vec:
            word_index = np.where(word_vec==word)[0][0]
            feature_row[word_index] = 1
    return feature_row

def generate_feature_vector(title_s, top_words, common_words):
    l = []
    for title in title_s:
        title_r = remove_common_words(title, common_words)
        l.append(create_feature_row(title_r, top_words))
    return l