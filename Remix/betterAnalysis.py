#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern

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

    print("This song has " + bpm + " bpm.")
    print("The rhythmic pattern is " + str(pattern))


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(filename)
