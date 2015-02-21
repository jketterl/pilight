'''
Created on Nov 21, 2012

@author: jketterl
'''

from . import Show
from audio import BeatDetector, BeatDelegate
import threading

class BPM(Show, BeatDelegate):
    def __init__(self):
        self.event = threading.Event()
        super(BPM, self).__init__()
    def run(self):
        detector = BeatDetector(self)
        detector.start()
        index = None
        fixtures = self.fixtureList.filter(lambda f : f.hasTag('rgb'))
        while (self.doRun):
            self.event.wait()
            if index is None:
                index = 0
            else:  
                fixtures[index].setChannels({'blue':0})
                index += 1
                if (index >= len(fixtures)): index = 0
            fixtures[index].setChannels({'blue':255})
            self.event.clear()
        fixtures[index].setChannels({'blue':0})
        detector.stop()
        self.endEvent.set()
    def onBeat(self):
        self.event.set()
    def stop(self):
        self.event.set()
        super(BPM, self).stop()
