import numpy as np
import pandas as pd

def normalize(column):
    mean = np.mean(column)
    sd = np.std(column)
    return column.apply(lambda d: (d-mean)/sd)

def bucketize(separators, num):
    for s in range(len(separators)):
        if num < separators[s]:
            return s
    return len(separators)

def accuracy(predicted_Y, Y):
    return sum(predicted_Y == Y)/float(len(predicted_Y))

def accuracy_on_set(df, theta, weights): 
    data = df[['num_comments', 'score']]
    X_data = data.num_comments
    Y_data = data.score.apply(lambda d: bucketize(cutoffs,d))
    prob_Y = pd.DataFrame(predict_values(X_data, thetas, weights))
    predicted_Y = prob_Y.apply(lambda d: d.argmax(), axis=1).rename('predicted')
    prob_Y.index = Y_data.index
    predicted_Y.index = Y_data.index
    #comparison = pd.concat([prob_Y, predicted_Y, Y, training_df.num_comments], axis=1)
    return accuracy(predicted_Y,Y_data)