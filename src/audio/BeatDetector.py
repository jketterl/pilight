'''
Created on Nov 21, 2012

@author: jketterl
'''

from .AudioReader import AudioReader
from .FFTReader import FFTReader
import threading, numpy, time
import math
from universe import Universe
from alsaaudio import ALSAAudioError

class CombFilter(object):
    def __init__(self, band, tempo):
        self.band = band
        self.tempo = tempo

        sampleRate = 48000.0 / 1024
        self.sampleCount = int(round(sampleRate / (float(tempo) / 60)))
        self.tempo = (sampleRate / self.sampleCount) * 60
        self.series = [0, self.sampleCount]
    def detect(self):
        backlog = self.band.backlog
        l = len(backlog) - 1

        if (l < self.sampleCount * 2): 
            return False
        
        delta = 0
        for i in range(self.sampleCount):
            delta += abs(backlog[l - i] - backlog[l - self.sampleCount - i])

        return delta / self.sampleCount

class Band(object):
    def __init__(self, number):
        self.number = number
        self.backlog = []
        #self.beat = False

        self.combs = []
        for bpm in range(100, 150, 5):
            self.combs.append(CombFilter(self, bpm))
    def update(self, value):
        self.backlog.append(value)
        while len(self.backlog) > 80: self.backlog.pop(0)
        '''
        average = numpy.average(self.backlog)
        v = 0.0
        for entry in self.backlog:
            v += entry
        v /= len(self.backlog)

        c = (-0.0025714 * v) + 1.5142857
        if value > average * c and not self.beat:
            #print '%d: BEAT' % self.number
            self.beat = True
        elif self.beat:
            self.beat = False
        '''

    def getBpm(self):
        best = False
        bestComb = False
        responses = []
        for comb in self.combs:
            response = comb.detect()
            if response is False: break
            responses.append(response)
            if best is False or response < best:
                best = response
                bestComb = comb
       
        if bestComb:
            #print "best match for band %d: %f BPM" % (self.number, bestComb.tempo)
            #print "best resopnse for band %d: %f, average: %f" % (self.number, best, numpy.average(responses))
            return (bestComb.tempo, numpy.mean(responses) - best)
        else:
            return (False, 0)
    def hasBeat(self):
        return self.beat
    def onValueChange(self, channel, value):
        self.update(value)

class BeatDetector(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        self.doRun = True
        self.BPM = 130
        super(BeatDetector, self).__init__()
    def run(self):
        beat = False
        
        universe = Universe(8)
        try:
            fftreader = FFTReader(AudioReader.instance("hw:1,0"), universe, 8)
            fftreader.start()
            pass

            bands = []
            for i in range(8):
                band = Band(i)
                bands.append(band)
                universe[i].valueCheck = False
                universe[i].addListener(band)
            
            lastTime = time.time()
            history = []
            while self.doRun:
                count = 0
                bpms = []
                weights = []
                for band in bands:
                    #if band.hasBeat(): count += 1
                    (bpm, weight) = band.getBpm()
                    if bpm is not False:
                        bpms.append(bpm)
                        weights.append(weight)
                if len(bpms) > 0:
                    #print bpms
                    #print weights
                    try:
                        bpm = numpy.average(bpms, weights=weights) * .97
                    except ZeroDivisionError:
                        bpm = 0
                else:
                    bpm = 0
                if (bpm > 0):
                    history.append(bpm)
                    while len(history) > 30: history.pop(0)
                    bpm = numpy.mean(history)
                    print "synthesizing %f BPM" % bpm
                    wait = 60 / bpm
                else:
                    wait = 2
                
                '''
                if count >= len(bands) / 2 and not beat:
                    self.delegate.onBeat()
                    beat = True
                elif beat:
                    beat = False
                '''

                self.delegate.onBeat()
                currentTime = time.time()
                wait += lastTime  - currentTime
                if wait > 0: time.sleep(wait)
                lastTime = currentTime + wait

            fftreader.stop()


        except ALSAAudioError:
            while self.doRun:
                time.sleep(.5)
                self.delegate.onBeat()
            
    def stop(self):
        self.doRun = False

class BeatDelegate(object):
    def onBeat(self):
        pass
