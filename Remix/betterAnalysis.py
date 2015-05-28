#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern, extractMeter, extractRhythm

usage = """
Usage: 
    python betterAnalysis.py <filename>

Example:
    python betterAnalysis.py mySong.mp3
"""

def main(filename):
    song = audio.LocalAudioFile(filename)

    bpm = extractBPM(song)
    pattern = extractRhythmicPattern(song)
    meter = extractMeter(song)
    rhythm = extractRhythm(song)

    print("This song has " + bpm + " bpm.")
    print("The rhythmic pattern is " + str(pattern))
    print("The time signature of this song is " + str(meter))
    print("The rhythm of this song is " + str(rhythm))
    #print(len(rhythm))



if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(filename)
