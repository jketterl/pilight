'''
Created on Nov 21, 2012

@author: jketterl
'''

from . import Show
from audio import BeatDetector, BeatDelegate
import threading, random, time

class Strobe(Show, BeatDelegate):
    def __init__(self, fixtures):
        self.event = threading.Event()
        super(Strobe, self).__init__(fixtures)
    def run(self):
        detector = BeatDetector(self)
        detector.start()
        while (self.doRun):
            self.event.wait()
            
            channel = random.randint(0, len(self.fixtures) - 1)

            colors = random.randint(1, 7)
            value = {}

            for color in ['red', 'green', 'blue']:
                value[color] = colors & 1
                colors = colors >> 1

            batch = []

            for i in range(channel, channel + 5):
                val = (3 - abs(channel + 2 - i)) * 255 / 3
                i = i % len(self.fixtures)
                out = {}
                for color in value:
                    out[color] = value[color] * val
                batch.append((self.fixtures[i], out))

            for (fixture, value) in batch:
                fixture.setChannels(value)
            time.sleep(.2)
            for (fixture, value) in batch:
                fixture.setChannels({'red':0,'green':0,'blue':0})
            
            self.event.clear()
        detector.stop()
        self.endEvent.set()
    def onBeat(self):
        self.event.set()
    def stop(self):
        self.event.set()
        super(Strobe, self).stop()
