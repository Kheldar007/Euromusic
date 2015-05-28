#!/usr/bin/python
# encoding: utf=8

# Genere les informations relatives a une certaine chanson.

usage = """
Usage: 
    python titleArtistDurationFromSong.py <song.mp3>

Example:
    python titleArtistDurationFromSong.py music.mp3
"""

import json, requests, shlex
from subprocess import Popen, PIPE


# @brief Generer une empreinte pour la musique.
# @param filesong Le nom du fichier.mp3.
def data(fileSong):
	cmd = "./fpcalc " + fileSong
	process = Popen(shlex.split(cmd), stdout = PIPE)
	data = process.communicate()
	exit_code = process.wait()
	result = data[0]
	
	return result

# @brief Extraire la duree de la musique.
# @param data L'identifiant et l'empreinte de la musique.
def duration(data):
	beginning = data.find("DURATION=") + len("DURATION=")
	ending = data.find("\nFINGERPRINT=")
	result = data[beginning:ending]
	
	return result
	
# @brief Afficher la duree de la chanson.
# @param artist La duree.
def printDuration(duration):
	print "Duree : " + duration + "s"

# @brief Extraire l'empreinte de la musique.
# @param data L'identifiant et l'empreinte de la musique.
def fingerprint(data):
	beginning = data.find("FINGERPRINT=") + len("FINGERPRINT=")
	result = data[beginning:]
	
	return result
	
# @brief Rechercher sur internet le lien correspondant a la musique.
# @param duration La duree.
# @param fingerprint L'empreinte.
def searchMusic(duration, fingerprint):	
	url = 'http://api.acoustid.org/v2/lookup?client=ULjKruIh&meta=sources+recordings&duration=' + duration + '&fingerprint=' + fingerprint # Rechercher les informations sur la chanson donnee.
	resp = requests.get(url=url)
	data = json.loads(resp.text) # data de type dictionnaire
	
	results = data["results"]
	recordings = results[0]["recordings"]
	
	sources = 0 # Nombre de sources pour un element du dictionnaire.
	index = 0 # Indice de l'element ayant le plus de sources.
	i = 0
	while i < len(recordings): # Parcourir le nombre de sources du dictionnaire.
		sources_t = recordings[i]["sources"]
		if sources_t > sources:
			sources = sources_t # Conserver le nouveau nombre si plus grand.
			index = i
		i = i + 1
		
	result = recordings[index] # L'element le plus pertinent.
	
	return result
	
# @brief Titre de la chanson.
# @param songData Les donnees relatives a la chanson.
def title(songData):
	result = songData["title"]
	
	return result
	
# @brief Afficher le titre.
# @param title Le titre.
def printTitle(title):
	print "Titre : " + title
	
# @brief Identifiant de la chanson.
# @param songData Les donnees relatives a la chanson.
def idRecording(songData):
	result = songData["id"]
	
	return result
	
# @brief Informations concernant l'artiste.
# @param songData Les donnees relatives a la chanson.
def artistsData(songData):
	result = songData["artists"][0]
	
	return result
	
# @brief Identifiant de l'artiste.
# @param artists L'artiste.
def idArtist(artists):
	result = artists["artists"]
	
	return result
	
# @brief Nom de l'artiste.
# @param artists L'artiste.
def nameArtist(artists):
	result = artists["name"]
	
	return result
	
# @brief Afficher le nom de l'artiste.
# @param artist Le nom de l'artiste.
def printArtist(artist):
	print "Artiste : " + artist


if __name__ == '__main__':
	import sys
	
	try:
		song = sys.argv[1]
	except:
		print usage
		sys.exit(-1)
