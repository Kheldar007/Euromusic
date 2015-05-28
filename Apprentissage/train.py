#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern, extractMeter
from glob import glob
from sklearn import svm
#from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import time
import sys
import pyechonest.util

# for automatic testing
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn import cross_validation

usage = """
Usage: 
    python train.py <TrainDataFilename>

Example:
    python train.py songDataFull.tab
"""

def main(filename):
    target = []
    data = []
    with open(filename,'r') as f:
        for line in f:
            fields = line.split("\t")
            target.append(fields[1])
            features = {}
            features['bpm'] = fields[2]
            features['meter'] = fields[3].rstrip()
            features['rhythm'] = fields[4].rstrip()
            header_length = 5
            if len(fields) > header_length:
                for i in range(8):
                    features['rhythm' + str(i)] = fields[i+header_length].rstrip()
            
            data.append(features)
                

    ### Do the training ###
    vec = DictVectorizer()
    data = vec.fit_transform(data).toarray()
    target = np.asarray(target)
    #clf = GaussianNB()
    clf = svm.SVC(gamma=0.001, C=100.) # parameters to be verified
    #clf.fit(data[:-1], target[:-1]) # learn from the data
    

    data_train, data_test, target_train, target_test = train_test_split(data, target)
    print("Splitted the data. Now learning ...")
    clf.fit(data_train, target_train) # learn from the data
    print("Learned from the data. Now predicting ...")
    
    joblib.dump(vec, 'vectorizer.pkl')
    joblib.dump(clf, 'danceModel.pkl')

    ### Testing ###

    #target_pred = cross_validation.cross_val_predict(clf, data, target, cv=10)
    #conf_matrix = confusion_matrix(target, target_pred)
    #score = metrics.accuracy_score(target, target_pred)

    #print(conf_matrix)
    #print(score)

    scores = cross_validation.cross_val_score(clf, data, target, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))



if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(filename)
