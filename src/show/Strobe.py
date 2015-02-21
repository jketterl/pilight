from . import Show
import time

class Strobe(Show):
    def __init__(self, *args, **kwargs):
        super(Strobe, self).__init__(*args, **kwargs)
    def run(self):
        self.fixtures = self.fixtureList.filter(lambda f : f.hasTag('rgb'))
        while self.doRun:
            self.setValue(255)
            time.sleep(.05)
            self.setValue(0)
            time.sleep(.1)
        self.endEvent.set()
    def setValue(self, value):
        for fixture in self.fixtures:
            fixture.setChannels({'red':value,'green':value,'blue':value})
