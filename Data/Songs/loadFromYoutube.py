#!/usr/bin/python
# encoding: utf=8

from __future__ import unicode_literals
import youtube_dl

usage = """
Usage: 
    python loadFromYoutube.py <URL>

Example:
    python 'http://www.youtube.com/watch?v=BaW_jenozKc'
"""

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def main(urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) == 1:
        print usage
        sys.exit(-1)

    urls = sys.argv[1:]
    main(urls)
