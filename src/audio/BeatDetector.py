'''
Created on Nov 21, 2012

@author: jketterl
'''

from audio.AudioReader import AudioReader
import threading, numpy, struct

class Band(object):
    def __init__(self, number):
        self.number = number
        self.backlog = []
        self.beat = False
    def update(self, data):
        powers = numpy.average(numpy.power(data, 2))
        self.backlog.append(powers)
        while len(self.backlog) > 50: self.backlog.pop(0)
        if powers > numpy.average(self.backlog) * 1.3 and not self.beat:
            #print '%d: BEAT' % self.number
            self.beat = True
        elif self.beat:
            self.beat = False
    def hasBeat(self):
        return self.beat

class BeatDetector(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        self.doRun = True
        self.BPM = 130
        super(BeatDetector, self).__init__()
    def run(self):
        audioreader = AudioReader.instance()
        #audioreader.start()
        
        beat = False
        
        bands = []
        for i in range(64):
            bands.append(Band(i))
        
        while self.doRun:
            audioreader.event.wait()
            audioreader.event.clear()
            
            form = '<%dh' % (audioreader.l * 2)
            data = struct.unpack(form, audioreader.data)
            
            #start = time.time()
            fft = numpy.abs(numpy.fft.fft(data))
            fft = fft[0:len(fft)/2]
            ratio = float(len(fft)) / len(bands)
            for index, band in enumerate(bands):
                band.update(fft[int(index * ratio):int((index + 1) * ratio)])
            
            #elapsed = time.time() - start
            #print 'fft time is: ' + str(elapsed)
            
            count = 0
            for band in bands:
                if band.hasBeat(): count += 1
                
            if count > 32 and not beat:
                self.delegate.onBeat()
                beat = True
            elif beat:
                beat = False
            
            
        #audioreader.stop()
    def stop(self):
        self.doRun = False

class BeatDelegate(object):
    def onBeat(self):
        pass