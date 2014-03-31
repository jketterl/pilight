from . import Show
import time
from fixture import FixtureManager

class Strobe(Show):
    def __init__(self, start, end):
        super(Strobe, self).__init__()
    def run(self):
        self.fixtures = FixtureManager.filter(lambda f : f.hasTag('rgb', 'dimmer'))
        while self.doRun:
            self.setValue(255)
            time.sleep(.05)
            self.setValue(0)
            time.sleep(.1)
        self.endEvent.set()
    def setValue(self, value):
        for fixture in self.fixtures:
            fixture.setChannels({'red':value,'green':value,'blue':value})
