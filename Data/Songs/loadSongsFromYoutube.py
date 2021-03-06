#!/usr/bin/python
# encoding: utf=8

usage = """
Usage: 
    python loadFromYoutube.py <song data file> <outputfolder> [(optional) line number to restart]

Example:
    python loadFromYoutube.py songData.tab ./chansons/ [29]
"""


def main(filename, outputfolder, songToRestart):    
    songs = []
    with open(filename, 'r') as f:
        for line in f:
            entries = line.split("\t")
            songs.append(entries[0] + " " + entries[1])

    loadSongs(songs, outputfolder.strip("/"), songToRestart)


def loadSongs(songs, outputfolder, songToRestart):
    import urllib
    import json as m_json
    import re
    import time
    import subprocess
    from random import randint
    import getpass
    from time import sleep

    song_num = 1
    for song in songs:
        if (song_num < songToRestart):
            song_num += 1
            continue

        query = song
        query = urllib.urlencode ( { 'q' : query } )
        response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
        json = m_json.loads ( response )
        results = []
        # Try googling twice
        if json [ 'responseData' ] != None:
            results = json [ 'responseData' ] [ 'results' ]
        else:
            print "Google ne nous aime plus. Alors, on attend 30 seconds ..."
            sleep(30)
            print "Et on reprend!"
            response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
            json = m_json.loads ( response )
            results = json [ 'responseData' ] [ 'results' ]
            
        for result in results:
            title = result['title']
            url = result['url']
            if re.search(r'www.youtube.com',url):
                print ( title + '; ' + url )
                print "DOWNLOADING",title
                decoded_url=urllib.unquote(url).decode('utf8')
                print decoded_url
                subprocess.call(['youtube-dl','-o',outputfolder+'/'+str(song_num)+'_%(title)s.(ext)s',"--extract-audio","--audio-format","mp3",decoded_url])
                break;
        print song_num
        time.sleep(randint(10,15))
        song_num+=1

if __name__ == '__main__':
    import sys
    
    if (len(sys.argv) != 3 and len(sys.argv) != 4):
        print usage
        sys.exit(-1)

    filename = sys.argv[1]
    outputfolder = sys.argv[2]
    main(filename, outputfolder, int(sys.argv[3]) if len(sys.argv) == 4 else 1)
