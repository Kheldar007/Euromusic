#!/usr/bin/python
# encoding: utf-8

from glob import glob
import os
import echonest.remix.audio as audio
from featureExtraction import extractBPM
import titleArtistDurationFromSong as mbrainz
from classify import classify
import subprocess

from createDataBase import createDataBase
import sqlite3

usage = """
Usage: 
    python main.py <DossierDesChansons>

Example:
    python main.py ~/Musique/
"""

def main(dirName):
    songs = songSearch(dirName)

    createDataBase()

    conn = sqlite3.connect('songs.db')
    print "Opened database successfully";

    for filename in songs:
        subprocess.call(['sox', filename, filename+'_extract.wav', 'trim', '30', '30'])

        song = None
        while (song == None):
            try:
                song = audio.LocalAudioFile(filename+'_extract.wav')
            except pyechonest.util.EchoNestAPIError:
                print("Echo Nest lets us wait a bit. I'll sleep one minute ...")
                time.sleep(60)
                continue
            except:
                e = sys.exc_info()[0]
                print("%s" % e)
                print("I will sleep 10 seconds and try again ...")
                time.sleep(10)


        subprocess.call(['rm', filename+'_extract.wav'])

        bpm = extractBPM(song) # 4
        data = mbrainz.data(filename)
        duration = mbrainz.duration(data) # 3
        songData = mbrainz.searchMusic(duration, mbrainz.fingerprint(data))
        artist = mbrainz.nameArtist(mbrainz.artistsData(songData)) # 2
        title = mbrainz.title(songData) # 1
        dance = classify('danceModel.pkl', 'vectorizer.pkl', song) # 5

        statement = "INSERT INTO Song (Title,Duration,Bpm,Artist,DanceName,FilePath) VALUES ('"+title+"', "+ str(duration)+", "+ str(bpm)+", '"+artist+"', '"+dance+'\', "'+os.path.abspath(filename)+'");'
        #print statement
        conn.execute(statement)

        #print (title, artist, duration, bpm, dance)

    conn.commit()
    print "Records created successfully";
    conn.close()

    
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
