'''
Created on Nov 21, 2012

@author: jketterl
'''

from .AudioReader import AudioReader
from .FFTReader import FFTReader
import threading, numpy, time
import math
from universe import Universe

class Band(object):
    def __init__(self, number):
        self.number = number
        self.backlog = []
        self.beat = False
    def update(self, value):
        self.backlog.append(value)
        while len(self.backlog) > 50: self.backlog.pop(0)
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
        fftreader = FFTReader(AudioReader.instance("hw:1,0"), universe, 8)
        fftreader.start()

        bands = []
        for i in range(8):
            band = Band(i)
            bands.append(band)
            universe[i].addListener(band)
        
        while self.doRun:
            count = 0
            for band in bands:
                if band.hasBeat(): count += 1

            if count >= len(bands) / 2 and not beat:
                self.delegate.onBeat()
                beat = True
            elif beat:
                beat = False

            time.sleep(.1)

        fftreader.stop()
            
    def stop(self):
        self.doRun = False

class BeatDelegate(object):
    def onBeat(self):
        pass
