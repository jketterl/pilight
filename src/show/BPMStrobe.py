'''
Created on Nov 21, 2012

@author: jketterl
'''

from . import Show
from audio import BeatDetector, BeatDelegate
import threading, random, time

class Bleep(object):
    def __init__(self, fixtures, position, color):
        self.fixtures = fixtures
        self.position = position
        self.color = color
        self.initialRange = 1
        self.range = self.initialRange
        self.initialBrightness = 255
        self.brightness = self.initialBrightness

        self.show()
    def show(self):
        batch = []
        delta = int(self.range -1 / 2)
        for i in range(self.position - delta, self.position + delta):
            val = (delta + 1 - abs(self.position - i)) * self.brightness / (delta + 1)
            i = i % len(self.fixtures)
            out = {}
            for color in self.color:
                out[color] = self.color[color] * val
            batch.append((self.fixtures[i], out))

        for (fixture, value) in batch:
            fixture.setChannels(value)

    def dismiss(self):
        delta = int(self.range -1 / 2)
        for i in range(self.position - delta, self.position + delta):
            i = i % len(self.fixtures)
            self.fixtures[i].setChannels({'red':0,'green':0,'blue':0})
        
    def spread(self):
        self.range += 2
        self.brightness -= 20
        if self.brightness < 0: self.brightness = 0
        if self.range > len(self.fixtures): self.range = len(self.fixtures)
        self.show()

class BPMStrobe(Show, BeatDelegate):
    def __init__(self, fixtures):
        self.event = threading.Event()
        super(BPMStrobe, self).__init__(fixtures)
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

            b = Bleep(self.fixtures, channel, value)

            self.event.clear()

            while not self.event.is_set():
                self.event.wait(.01)
                b.spread()
       
            b.dismiss()
        detector.stop()
        self.endEvent.set()
    def onBeat(self):
        self.event.set()
    def stop(self):
        self.event.set()
        super(BPMStrobe, self).stop()
