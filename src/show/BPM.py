'''
Created on Nov 21, 2012

@author: jketterl
'''

from . import Show
from audio import BeatDetector, BeatDelegate
import threading

class BPM(Show, BeatDelegate):
    def __init__(self, fixtures):
        self.event = threading.Event()
        self.fixtures = fixtures
        super(BPM, self).__init__()
    def run(self):
        detector = BeatDetector(self)
        detector.start()
        index = None
        while (self.doRun):
            self.event.wait()
            if index is None:
                index = 0
            else:  
                self.fixtures[index].setChannels({'blue':0})
                index += 1
                if (index >= len(self.fixtures)): index = 0
            self.fixtures[index].setChannels({'blue':255})
            self.event.clear()
        self.fixtures[index].setChannels({'blue':0})
        detector.stop()
        self.endEvent.set()
    def onBeat(self):
        self.event.set()
    def stop(self):
        self.event.set()
        super(BPM, self).stop()
