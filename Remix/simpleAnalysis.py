#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio

usage = """
Usage: 
    python simpleAnalysis.py <filename>

Example:
    python one.py mySong.mp3
"""

def main(filename):
    song = audio.LocalAudioFile(filename)
    tempo = song.analysis.tempo
    bpm = "%.0f" % round(tempo['value'])
    confidence = "%0.1f" % (tempo['confidence']*100)
    print("With an accuracy of " + confidence + " % this song has " + bpm + " bpm.")


if __name__ == '__main__':
    import sys
    try:
        filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(filename)
