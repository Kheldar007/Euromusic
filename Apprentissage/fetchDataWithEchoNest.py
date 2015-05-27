#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio
from featureExtraction import extractBPM, extractRhythmicPattern, extractMeter
from glob import glob
import time
import sys
import pyechonest.util

usage = """
Usage: 
    python train.py <TrainDataFilename> <SongFileDirectory>

Example:
    python train.py songData.tab chansons/
"""

def main(filename, dirName):
    target = []
    data = []
    with open(filename, 'r') as f:
        num = 1
        for line in f:
            songFileNames = glob(dirName.rstrip('/') + '/' + str(num) + '_*')

            if len(songFileNames) == 0:
                print("There's no song for number " + str(num))
                num += 1
                continue
            if len(songFileNames) > 1:
                print("Warning: We found too much songs for number " + str(num))

            print("We found " + songFileNames[0] + " for number " + str(num))

            song = None
            while (song == None):
                try:
                    song = audio.LocalAudioFile(songFileNames[0])
                except pyechonest.util.EchoNestAPIError:
                    print("Echo Nest lets us wait a bit. I'll sleep one minute ...")
                    time.sleep(60)
                    continue
                except:
                    e = sys.exc_info()[0]
                    print("%s" % e)
                    print("I will sleep 10 seconds and try again ...")
                    time.sleep(10)

            bpm = extractBPM(song)
            meter = extractMeter(song)
            if bpm <= 0 or meter <= 0:
                print("Skipping song number " + str(num) + " because of insufficient analysis.")
                num += 1
                continue

            #rhythm = extractRhythmicPattern(song)
            #m = max(rhythm)
            #indexes = [i for i, j in enumerate(rhythm) if j == m]
            #if len(rhythm) != 8:
            data.append({'num':num, 'bpm':bpm, 'meter':meter})#, 'maxTone':indexes[0]})
            #else:
                #data.append({'bpm':bpm, 'meter':meter, 'rhythm0':rhythm[0], 'rhythm1':rhythm[1], 'rhythm2':rhythm[2], 'rhythm3':rhythm[3], 'rhythm4':rhythm[4], 'rhythm5':rhythm[5], 'rhythm6':rhythm[6], 'rhythm7':rhythm[7]})
            

            target.append(line.split("\t")[2].rstrip())
            num += 1


    ### Saving what we've got from Echo Nest ###
    with open('songDataFull.tab', 'w') as f:
        for i in range(len(target)):
            f.write(str(data[i]['num']))
            f.write("\t")
            f.write(str(target[i]))
            f.write("\t")
            f.write(str(data[i]['bpm']))
            f.write("\t")
            f.write(str(data[i]['meter']))
            #f.write("\t")
            #f.write(str(data[i]['maxTone']))
            if 'rhythm0' in data[i]:
                f.write("\t")
                f.write(str(data[i]['rhythm0']))
                f.write("\t")
                f.write(str(data[i]['rhythm1']))
                f.write("\t")
                f.write(str(data[i]['rhythm2']))
                f.write("\t")
                f.write(str(data[i]['rhythm3']))
                f.write("\t")
                f.write(str(data[i]['rhythm4']))
                f.write("\t")
                f.write(str(data[i]['rhythm5']))
                f.write("\t")
                f.write(str(data[i]['rhythm6']))
                f.write("\t")
                f.write(str(data[i]['rhythm7']))
            f.write("\n")



if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        dirName = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(filename, dirName)
