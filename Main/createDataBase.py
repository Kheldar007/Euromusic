#!/usr/bin/python
# encoding: utf=8

# Cree une base de donnees details concernant les chansons contenues dans un
# dossier.

usage = """
Usage: 
    python createDataBase.py <path/>

Example:
    python createDataBase.py RepertoireDeChansons/
"""


if __name__ == '__main__':
	import sys
	
	try:
		folder = sys.argv[1]
	except:
		print usage
		sys.exit(-1)
