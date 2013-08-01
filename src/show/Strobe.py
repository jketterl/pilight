from . import Show
import time

class Strobe(Show):
    def __init__(self, fixtures, start, end):
        super(Strobe, self).__init__(fixtures)
        self.fixtures = fixtures[start:end]
    def run(self):
        while self.doRun:
            self.setValue(255)
            time.sleep(.05)
            self.setValue(0)
            time.sleep(.1)
        self.endEvent.set()
    def setValue(self, value):
        for fixture in self.fixtures:
            fixture.setChannels({'red':value,'green':value,'blue':value})
