from . import Show
import threading, random

class Lichterkette(Show):
    def __init__(self, *args, **kwargs):
        super(Lichterkette, self).__init__(*args, **kwargs)
        self.shouldEnd = threading.Event()
        self.fixtures = self.fixtures[64:]
    def run(self):
        for f in self.fixtures:
            f.setChannels(self.getRandomColor())
        while self.doRun and not self.shouldEnd.isSet():
            random.choice(self.fixtures).setChannels(self.getRandomColor())
            self.shouldEnd.wait(random.random())
        for f in self.fixtures:
            f.setChannels({"red":0, "green":0, "blue":0})
        self.endEvent.set()
    def getRandomColor(self):
        channel = random.randint(0, len(self.fixtures) - 1)

        colors = random.randint(1, 6)
        value = {}

        for color in ['red', 'green', 'blue']:
            value[color] = (colors & 1) * 127
            colors = colors >> 1
        return value
    def stop(self):
        self.shouldEnd.set()
