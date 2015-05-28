#!/usr/bin/python
# encoding: utf=8

# Cree une base de donnees details concernant les chansons contenues dans un
# dossier.

import sqlite3

usage = """
Usage: 
    python createDataBase.py <path/>

Example:
    python createDataBase.py ../Data/
"""

# @brief Creer une table pour les chansons.
def createTableSong():
	return "CREATE TABLE Song (Title VARCHAR(128), Duration INT, Bpm INT, Artist VARCHAR(128), DanceName VARCHAR(128));"

# @brief Creer une table pour conserver les chansons.
def createTableArtist():
	return "CREATE TABLE Artist (Id VARCHAR(128), Name VARCHAR(128), PRIMARY KEY (Id));"

# @brief Creer une table pour conserver les chansons.
def createTableDance():
	return "CREATE TABLE Dance (Name VARCHAR(128), Info VARCHAR(128), PRIMARY KEY (Name));"
	
# @brief Creer la banque de donnees.
def createDataBase():
	connexion = sqlite3.connect('songs.db')

	connexion.execute(createTableSong())
	#connexion.execute(createTableArtist())
	#connexion.execute(createTableDance())

	connexion.commit()
	connexion.close()


if __name__ == '__main__':
	import sys
	
	try:
		folder = sys.argv[1]
		# database = open ("songs.sql" , "w") # Creer/ecraser le fichier .sql.
		# 
		# database.write(createTableSong())
		# database.write(createTableArtist())
		# database.write(createTableDanse())
		# 
		# database.close()
		
		createDataBase()
	except:
		sys.exit(-1)
