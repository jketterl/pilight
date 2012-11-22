'''
Created on Nov 21, 2012

@author: jketterl
'''

from audio.AudioReader import AudioReader
import threading, numpy, struct

class BeatDetector(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        self.doRun = True
        self.BPM = 130
        super(BeatDetector, self).__init__()
    def run(self):
        audioreader = AudioReader.instance()
        #audioreader.start()
        
        backlog = []
        beat = False
        
        while self.doRun:
            audioreader.event.wait()
            audioreader.event.clear()
            
            form = '<%dH' % (audioreader.l * 2)
            data = numpy.array(struct.unpack(form, audioreader.data), dtype='h')
            
            powers = numpy.power(data, 2)
            powers = numpy.average(powers)
            if powers < 0: continue
            
            backlog.append(powers)
            while len(backlog) > 50: backlog.pop(0)

            if powers > numpy.average(backlog) * 1.3 and not beat:
                self.delegate.onBeat()
                beat = True
            else:
                beat = False
        #audioreader.stop()
    def stop(self):
        self.doRun = False

class BeatDelegate(object):
    def onBeat(self):
        pass