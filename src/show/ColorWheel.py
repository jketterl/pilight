from . import Show
import time, colorsys

class ColorWheel(Show):
    def __init__(self, fixtures):
        self.count = len(fixtures)
        self.relation = 4
        self.wheelCount = self.count * self.relation

        self.wheel = [0] * self.wheelCount
        for i in range(self.wheelCount):
            hue = float(i) / self.wheelCount
            color = dict(zip(('red', 'green', 'blue'), colorsys.hsv_to_rgb(hue, 1, 1)))
            for channel in color:
                color[channel] = int(round(color[channel] * 255))
            self.wheel[i] = color

        super(ColorWheel, self).__init__(fixtures)

    def run(self):
        offset = 0
        while self.doRun:
            batch = []
            for i in range(self.count):
                position = int(round(offset + i * self.relation)) % self.wheelCount
                #self.fixtures[i].setChannels(self.wheel[position]);
                batch.append((self.fixtures[i], self.wheel[position]));
            for (channel, value) in batch:
                channel.setChannels(value)
            offset = (offset + 1) % self.wheelCount
            time.sleep(.02)
        for i in range(self.count):
            self.fixtures[i].setChannels({'red':0,'green':0,'blue':0})
        self.endEvent.set()
