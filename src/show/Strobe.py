from . import Show
import time

class Strobe(Show):
    def run(self):
        while self.doRun:
            self.setValue(255)
            time.sleep(.05)
            self.setValue(0)
            time.sleep(.1)
        self.endEvent.set()
    def setValue(self, value):
        for fixture in self.fixtures[60:63]:
            fixture.setChannels({'red':value,'green':value,'blue':value})
