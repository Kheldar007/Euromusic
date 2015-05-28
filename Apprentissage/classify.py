#!/usr/bin/python
# encoding: utf=8

from sklearn.externals import joblib
import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythm, extractMeter
from sklearn.feature_extraction import DictVectorizer


usage = """
Usage: 
    python classify.py <ModelFilename> <VectorizerFilename> <SongFile>

Example:
    python train.py danceModel.pkl vectorizer.pkl mySong.mp3
"""

def classify(modelFile, vecFile, songFile):
    clf = joblib.load(modelFile)
    vec = joblib.load(vecFile)
    song = audio.LocalAudioFile(songFile)

    rhythm = extractRhythm(song, N=1)

    #if len(rhythm) != 8:
    data = {'bpm':extractBPM(song), 'meter':extractMeter(song), 'rhythm':rhythm[0]}
    #else:
    #    data = {'bpm':extractBPM(song), 'meter':extractMeter(song), 'rhythm0':rhythm[0], 'rhythm1':rhythm[1], 'rhythm2':rhythm[2], 'rhythm3':rhythm[3], 'rhythm4':rhythm[4], 'rhythm5':rhythm[5], 'rhythm6':rhythm[6], 'rhythm7':rhythm[7]}


    data = vec.transform([data]).toarray()

    return clf.predict(data)[0]

def main(filename, vecName, dirName):
    print(classify(filename, vecName, dirName))

if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        vecName = sys.argv[2]
        dirName = sys.argv[3]
    except:
        print usage
        sys.exit(-1)
    main(filename, vecName, dirName)
