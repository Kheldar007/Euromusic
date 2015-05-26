#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern, extractMeter
from glob import glob
#from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import time
import sys

usage = """
Usage: 
    python train.py <TrainDataFilename> <SongFileDirectory>

Example:
    python train.py songData.tab chansons/
"""

def main(filename, dirName):
    target = []
    data = []
    with open(filename, 'r') as f:
        num = 1
        for line in f:
            songFileNames = glob(dirName.rstrip('/') + '/' + str(num) + '_*')

            if len(songFileNames) == 0:
                print("There's no song for number " + str(num))
                num += 1
                continue
            if len(songFileNames) > 1:
                print("Warning: We found too much songs for number " + str(num))

            print("We found " + songFileNames[0] + " for number " + str(num))

            song = None
            while (song == None):
                try:
                    song = audio.LocalAudioFile(songFileNames[0])
                except:
                    e = sys.exc_info()[0]
                    print("%s" % e)
                    print("I will sleep 30 seconds ...")
                    time.sleep(30)

            rhythm = extractRhythmicPattern(song)
            if len(rhythm) != 8:
                data.append({'bpm':extractBPM(song), 'meter':extractMeter(song)})
            else:
                data.append({'bpm':extractBPM(song), 'meter':extractMeter(song), 'rhythm0':rhythm[0], 'rhythm1':rhythm[1], 'rhythm2':rhythm[2], 'rhythm3':rhythm[3], 'rhythm4':rhythm[4], 'rhythm5':rhythm[5], 'rhythm0':rhythm[6], 'rhythm0':rhythm[7]})
            

            target.append(line.split("\t")[2].rstrip())
            num += 1

    vec = DictVectorizer()
    data = vec.fit_transform(data).toarray()
    clf = GaussianNB()
    #clf = svm.SVC(gamma=0.001, C=100.) # parameters to be verified
    clf.fit(data[:-1], np.asarray(target[:-1])) # learn from the data
    
    joblib.dump(vec, 'vectorizer.pkl')
    joblib.dump(clf, 'danceModel.pkl')


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        dirName = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(filename, dirName)
