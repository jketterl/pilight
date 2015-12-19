from . import Show
import threading, random

class Lichterkette(Show):
    def __init__(self, *args, **kwargs):
        super(Lichterkette, self).__init__(*args, **kwargs)
        self.shouldEnd = threading.Event()
        self.fixtures = self.fixtureList.filter(lambda f : f.hasTag('rgb'))
        self.brightness = 255
    def run(self):
        count = len(self.fixtures)
        map = [self.getRandomColor() for i in range(0, count)]
        while self.doRun and not self.shouldEnd.isSet():
            map[random.randint(0, count - 1)] = self.getRandomColor()
            for i, c in enumerate(map):
                self.fixtures[i].setChannels(self.scale(c))
            self.shouldEnd.wait(random.random())
        for f in self.fixtures:
            f.setChannels({"red":0, "green":0, "blue":0})
        self.endEvent.set()
    def getRandomColor(self):
        channel = random.randint(0, len(self.fixtures) - 1)

        colors = random.randint(1, 6)
        value = {}

        for color in ['red', 'green', 'blue']:
            value[color] = (colors & 1)
            colors = colors >> 1
        return value
    def scale(self, c):
        out = {}
        for color in ['red', 'green', 'blue']:
            out[color] = c[color] * self.brightness
        return out
    def stop(self):
        self.shouldEnd.set()
    def setParams(self, brightness = None, **kwargs):
        if brightness is not None:
            self.brightness = brightness
