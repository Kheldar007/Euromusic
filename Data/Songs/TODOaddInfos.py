#!/usr/bin/python
# encoding: utf=8


# Add infos to the list of songs.


import echonest.remix.audio as audio
import glob
from fetchSongList import doTheWork , main


# @param songName A song .mp3.
# @param songList A list of songs, .tab file.
def writeBpm (songName , songList):
	song = audio.LocalAudioFile(songName)
	bpm = "%.0f" % round(song.analysis.tempo['value']) # Find the bpm value of the song in a string.
	
	songNumberString = ""
	for c in songName:
		if c == '_':
			break
		songNumberString += c
	songNumber = int(songNumberString) # Number of the song.
	
	i = 0
	for lines in songList:
		i += 1
		
		if(i == songNumber): # We found the song.
			print("yeaaah")
			lines = lines + "	" + bpm # Write the bpm value next to the song.
			
			break


if __name__ == '__main__':
	# main ()
	
	songs            = open("songData.tab" , "r")
	songsWithDetails = open("songDataDetails.tab" , "r")
	
	for lines in songs:
		songsWithDetails.write (lines) # Copy the songData file into songDataDetails
	
	for mp3Songs in glob.glob('*.mp3'):
		writeBpm(mp3Songs , songsWithDetails)
		
	songs.close()
	songsWithDetails.close()
