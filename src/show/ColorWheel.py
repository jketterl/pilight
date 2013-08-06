from . import Show
import time, colorsys
from control import Controllable

class ColorWheel(Controllable, Show):
    def __init__(self, fixtures):
        self.count = len(fixtures)
        self.relation = 4
        self.wheelCount = self.count * self.relation

        self.saturation = 1
        self.value = 1
        self.speed = .5

        self.generateWheel()
        super(ColorWheel, self).__init__(fixtures)
    def generateWheel(self):
        wheel = [0] * self.wheelCount
        for i in range(self.wheelCount):
            hue = float(i) / self.wheelCount
            color = dict(zip(('red', 'green', 'blue'), colorsys.hsv_to_rgb(hue, self.saturation, self.value)))
            for channel in color:
                color[channel] = int(round(color[channel] * 255))
            wheel[i] = color

        self.wheel = wheel

    def run(self):
        offset = 0
        while self.doRun:
            if self.wheel is None: self.generateWheel()
            wheel = self.wheel
            batch = []
            for i in range(self.count):
                position = int(round(offset + i * self.relation)) % self.wheelCount
                #self.fixtures[i].setChannels(wheel[position]);
                batch.append((self.fixtures[i], wheel[position]));
            for (channel, value) in batch:
                channel.setChannels(value)
            offset = (offset + 1) % self.wheelCount
            time.sleep(.01 / self.speed if self.speed > 0 else 1)
        for i in range(self.count):
            self.fixtures[i].setChannels({'red':0,'green':0,'blue':0})
        
        self.unregister()
        self.endEvent.set()

    def setParams(self, saturation = None, value = None, speed = None, **kwargs):
        if not saturation is None:
            self.saturation = saturation / 100.0
            self.wheel = None
        if not value is None:
            self.value = value / 100.0
            self.wheel = None
        if not speed is None:
            self.speed = speed / 100.0

    def getId(self):
        return 'colorwheel'
