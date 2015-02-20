from . import Show
from threading import Event, Thread
import random, time

class PoliceLight(Thread):
    def __init__(self, fixtures, pos, size, color, delay):
        super(PoliceLight, self).__init__()
        self.selectedFixtures = fixtures
        self.color = color
        self.pos = pos
        self.size = size
        self.reposition()
        self.delay = delay
        self.doRun = True
        self.event = Event()

        self.start()
    def run(self):
        countdown = 5;
        while (self.doRun):
            countdown -= 1
            if (countdown < 0):
                self.reposition()
                countdown = 5
            self.setValue(255)
            self.event.wait(.4)
            self.setValue(0)
            self.event.wait(.5)
            self.setValue(255)
            self.event.wait(.02)
            self.setValue(0)
            self.event.wait(self.delay + random.random() * .10 - .05)
        self.setValue(0)
    def reposition(self):
        self.pos += 1
        if (self.pos > len(self.selectedFixtures)):
            self.pos = 0
        self.fixtures = self.selectedFixtures[self.pos+0*self.size:self.pos+1*self.size]
    def setValue(self, v):
        for f in self.fixtures: f.setChannels({self.color:v})
        
    def stop(self):
        self.doRun = False
        self.event.set()

class Police(Show):
    def __init__(self, *args, **kwargs):
        super(Police, self).__init__(*args, **kwargs)
        self.event = Event() 
    def run(self):
        lights = []
        fixtures = self.fixtureList.filter(lambda f : f.hasTag('rgb'))
        for i in range(20):
            size = random.randint(1, 5)
            pos = random.randint(0, len(fixtures) - size * 3)
            lights.append(PoliceLight(fixtures, pos, size, 'red', .5))
            lights.append(PoliceLight(fixtures, pos + 2, size, 'blue', .6))
            time.sleep(random.random())

        self.event.wait()
        for l in lights: l.stop()
        self.endEvent.set()
    def stop(self):
        self.event.set()
        super(Police, self).stop()
