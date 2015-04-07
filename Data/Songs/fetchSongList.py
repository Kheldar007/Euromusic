#!/usr/bin/python
# encoding: utf=8

from __future__ import unicode_literals
from __future__ import print_function

#usage = """
#Usage: 
#    python fetchSongList.py <Newest chart number>
#
#Example:
#    python fetchSongList.py '201514'
#"""



def main():
    with open("songData.tab", 'w') as f:
        for dance in ['samba', 'cha-cha-cha', 'rumba', 'paso-doble', 'jive', 'langsamer-walzer', 'tango', 'wiener-walzer', 'foxtrott', 'salsa']:
            doTheWork(dance, f)


def doTheWork(nameOfDance, f):
    from bs4 import BeautifulSoup as bs
    from urllib2 import urlopen

    #soup = bs(urlopen('http://www.tanzmusik-online.de/charts/' + num))
    soup = bs(urlopen('http://www.tanzmusik-online.de/dance/'+nameOfDance+'/sort/date/order/desc/rating/5/'))
    
    for item in soup.findAll("div", { "class" : "item even"}) + soup.findAll("div", { "class" : "item odd"}):
        artist = item.find("span", {"class" : "artist"})
        title = item.find("div", {"class" : "title"})
        dance = item.find("div", {"class" : "dance"})
        
        print((("____" if artist == None else artist.a.text) + "\t" + ("____" if title == None else title.a.text) + "\t" + ("____" if dance == None else dance.div.text.strip())).encode('utf-8'), file=f)



if __name__ == '__main__':
    #import sys
    
    #if len(sys.argv) != 2:
    #    print(usage)
    #    sys.exit(-1)

    main()
