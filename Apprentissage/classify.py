#!/usr/bin/python
# encoding: utf=8

from sklearn.externals import joblib
import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern


usage = """
Usage: 
    python classify.py <ModelFilename> <SongFile>

Example:
    python train.py danceModel.pkl mySong.mp3
"""

def main(modelFile, songFile):
    clf = joblib.load(modelFile)
    song = audio.LocalAudioFile(songFile)
    data = (extractBPM(song), extractRhythmicPattern(song))
    print(clf.predict(data))


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
        dirName = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(filename, dirName)
