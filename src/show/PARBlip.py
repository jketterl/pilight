from . import Show
from audio import BeatDetector, BeatDelegate
from threading import Event
import random

class PARBlip(Show, BeatDelegate):
    def __init__(self):
        super(PARBlip, self).__init__()
        self.event = Event()
    def run(self):
        fixtures = self.fixtureList.filter(lambda f : f.hasTag('par'))

        detector = BeatDetector(self)
        detector.start();

        while (self.doRun):
            self.event.wait()
            for fixture in fixtures:
                fixture.setChannels(self.generateColor())
            self.event.clear()

        for fixture in fixtures:
            fixture.setChannels({'red':0, 'green':0, 'blue':0})

        detector.stop()
        self.endEvent.set()
    def generateColor(self):
        rs = random.randint(1, 7)
        value = {}

        for color in ['red', 'green', 'blue']:
            value[color] = (rs & 1) * 255
            rs = rs >> 1
        return value
    def onBeat(self):
        self.event.set()
    def stop(self):
        self.event.set()
        super(PARBlip, self).stop()
