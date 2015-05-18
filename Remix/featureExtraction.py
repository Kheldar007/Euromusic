#!/usr/bin/python
# encoding: utf=8

import echonest.remix.audio as audio

def getMostQuietChildIndex(quantum):
    min = quantum.children()[0]
    minIndex = 0
    index = 0
    for child in quantum.children():
        if child.mean_loudness() < min.mean_loudness():
            min = child
            minIndex = index
        index += 1
    
    return minIndex

def getLoudestChildIndex(quantum):
    max = quantum.children()[0]
    maxIndex = 0
    index = 0
    for child in quantum.children():
        if child.mean_loudness() > max.mean_loudness():
            max = child
            maxIndex = index
        index += 1
    
    return maxIndex

def getGreatestVolumeDifference(quantum):
    min = quantum.children()[getMostQuietChildIndex(quantum)]
    max = quantum.children()[getLoudestChildIndex(quantum)]
    return max.mean_loudness() - min.mean_loudness()


def getGreatestVolumeDifferencePair(quantum):
    min = getMostQuietChildIndex(quantum)
    max = getLoudestChildIndex(quantum)
    return (min, max)


def getTatumPeaks(bar, threshold=1.0):
    avg = bar.mean_loudness()*threshold
    peaks = []
    index = 0
    for beat in bar.children():
        for tatum in beat.children():
            if tatum.mean_loudness() > avg:
                peaks.append(index)
            index += 1
    
    return peaks

'''
get the two most common TwoTatumPeaks-Pattern par meter of a given song
map(lambda p: p[0], Counter(map (getHighestTwoTatumPeaks, song.analysis.bars)).most_common(2))
'''

def getHighestTwoTatumPeaks(bar):
    avg = bar.mean_loudness()
    childNum = len(bar.children())
    peaks = []
    index = 0
    for beat in bar.children():
        if index == 0 and childNum > 1:
            index = 2
            continue
        for tatum in beat.children():
            peaks.append((tatum.mean_loudness(), index))
            index += 1
    
    s_peaks = sorted(peaks, key=lambda p: p[0], reverse=True)
    return (s_peaks[0][1], s_peaks[min(2, childNum-1)][1])


def extractBPM(song):
    tempo = song.analysis.tempo
    bpm = "%.0f" % round(tempo['value'])
    return bpm


def extractRhythmicPattern(song):
    barPatterns = []
    meanLoudness = 0
    for bar in song.analysis.bars:
        meanLoudness += bar.mean_loudness()
        pattern = []
        for beat in bar.children():
            for tatum in beat.children():
                pattern.append(tatum.mean_loudness())
        barPatterns.append(pattern)

    rhythm = barPatterns[0]
    for barPattern in barPatterns[1:]:
        for i in range(0, len(barPattern)):
            rhythm[i] += barPattern[i]


    meanLoudness /= len(barPatterns)
    rhythm = map(lambda x: x/len(barPatterns), rhythm)
    rhythm = map(lambda x: x/meanLoudness - 1, rhythm)
    return rhythm
