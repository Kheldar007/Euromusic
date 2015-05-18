#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern
from glob import glob
from sklearn import svm
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
import numpy as np

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
            target.append(line.split("\t")[2].rstrip())
            songFileNames = glob(dirName.rstrip('/') + '/' + str(num) + '_*')

            if len(songFileNames) == 0:
                print("There's no song for number " + str(num))
                num += 1
                continue
            if len(songFileNames) > 1:
                print("Warning: We found too much songs for number " + str(num))

            print("We found " + songFileNames[0] + " for number " + str(num))

            song = audio.LocalAudioFile(songFileNames[0])
            data.append({'bpm':extractBPM(song), 'rhythm':extractRhythmicPattern(song)})
            num += 1

    vec = DictVectorizer()
    data = vec.fit_transform(data).toarray()
    clf = svm.SVC(gamma=0.001, C=100.) # parameters to be verified
    clf.fit(data[:-1], np.asarray(target[:-1])) # learn from the data
    
    joblib.dump(clf, 'danceModel.pkl')


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        dirName = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(filename, dirName)
