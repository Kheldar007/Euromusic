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

def extractMeter(song):
    meter = song.analysis.time_signature
    return meter['value']

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

    if len(song.analysis.bars) == 0:
        print("Warning: we found a song whose bars could not be analysed!")
        return []

    rhythm = barPatterns[0]
    for barPattern in barPatterns[1:]:
        for i in range(0, len(barPattern)):
            if (i >= len(rhythm)):
                rhythm.append(barPattern[i])
            else:
                rhythm[i] += barPattern[i]


    meanLoudness /= len(barPatterns)
    rhythm = map(lambda x: x/len(barPatterns), rhythm)
    rhythm = map(lambda x: x/meanLoudness - 1, rhythm)
    return rhythm



def decompress_string(compressed_string):
    import zlib, base64

    compressed_string = compressed_string.encode('utf8')
    if compressed_string == "":
        return None
    # do the zlib/base64 stuff
    try:
        # this will decode both url-safe and non-url-safe b64 
        actual_string = zlib.decompress(base64.urlsafe_b64decode(compressed_string))
    except (zlib.error, TypeError):
        print "Could not decode base64 zlib string %s" % (compressed_string)
        return None
    return actual_string

# Rhythmstring
# ------------ 
# With Analyzer v3.2 was introduced the rhythmstring, a binary representation of rhythmic impulses, or transients, over 8 
# frequency channels. The encoded format goes as follows:
# Fs Hop Nch <Nos Oi do_1 ... do_n> ... <Nos Oi do_1 ... do_n> 
# where: 
#    Fs: sampling rate 
#    Hop: hop size in samples
#    Nch: number of channels 
#    Nos: number of onsets 
#    Oi: initial onset frame 
#    do_n: number of frames to the next onset

def decode_string(s):
    #l = []
    #for i in range(0, len(s), 4):
    #    l.append(struct.unpack('<i', s[i:i+4]))
    #    print(l[-1])

    l = [int(i) for i in s.split(' ')]
    Fs = l.pop(0)
    Hop = l.pop(0)
    Nch = l.pop(0)
    liste = []
    n = 0
    for i in range(Nch):
        Nos = l[n]
        liste.append([])
        n += 2 # skip Nos and Oi
        for j in range(Nos-1):
            liste[i].append(l[n])
            n += 1

    return (Fs, liste)

### framerate = samplerate / number of channels
### duration = number of frames / framerate = nframes * nchannels / samplerate
### hypothesis: nchannels = 1

def extractRhythm(song, N=3):

    decompressed_string = decompress_string(song.analysis.rhythmstring)
    if decompressed_string == None:
        return None

    rhythms = decode_string(decompressed_string)
    rhythm = rhythms[1][0]

    for channel_string in rhythms[1][1:]:
        for i in range(len(channel_string)):
            if (i >= len(rhythm)):
                rhythm.append(channel_string[i])
            else:
                rhythm[i] += channel_string[i]

    rhythm = map(lambda x: float(x)/rhythms[0], rhythm)
    rhythm = map(lambda x: x/len(rhythms[1]), rhythm)

    #m = max(rhythm)
    #indexes = [i for i,j in enumerate(rhythm) if j == m]
    #print indexes

    import numpy as np
    return np.argsort(rhythm)[::-1][:N]

    #return rhythm
