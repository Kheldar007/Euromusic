#!/usr/bin/python
# encoding: utf-8

from glob import glob
import os
import echonest.remix.audio as audio
from featureExtraction import extractBPM
import titleArtistDurationFromSong as mbrainz
from classify import classify
import subprocess

usage = """
Usage: 
    python <DossierDesChansons>

Example:
    python ~/Musique/
"""

def main(dirName):
    songs = songSearch(dirName)

    for filename in songs:
        subprocess.call(['sox', filename, filename+'_extract.wav', 'trim', '30', '10'])

        song = audio.LocalAudioFile(filename+'_extract.wav')
        bpm = extractBPM(song) # 4
        data = mbrainz.data(filename)
        duration = mbrainz.duration(data) # 3
        songData = mbrainz.searchMusic(duration, mbrainz.fingerprint(data))
        artist = mbrainz.nameArtist(mbrainz.artistsData(songData)) # 2
        title = mbrainz.title(songData) # 1
        dance = classify('danceModel.pkl', 'vectorizer.pkl', filename) # 5

        print (title, artist, duration, bpm, dance)

    
def songSearch(dirName):
    songs = glob(dirName.rstrip('/') + '/*.wav') + glob(dirName.rstrip('/') + '/*.mp3')

    for root, dirs, files in os.walk(dirName):
        for subdir in dirs:
            songs.extend(songSearch(subdir))

    return songs


if __name__ == '__main__':
    import sys
    try:
        dirName = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(dirName)
