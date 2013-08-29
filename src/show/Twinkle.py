from . import Show
import time
import colorsys
import random

class Twinkle(Show):
    def __init__(self, *args, **kwargs):
        super(Twinkle, self).__init__(*args, **kwargs)
        self.hue = .05
        self.saturation = 1
        self.value = 1
        self.twinkles = []
    def run(self):
        baseColor = self.hsv_to_rgb(self.hue, self.saturation, self.value * .1)
        for f in self.fixtures:
            f.setChannels(baseColor)
        while self.doRun:
            target = self.value * .1
            if (random.random() < .1):
                pos = random.randint(0, len(self.fixtures) - 1)
                val = float(self.value) * (random.random() * .9 + .1)
                self.twinkles.append({'fixture':self.fixtures[pos], 'value':val})

            toDelete = []
            for index, twinkle in enumerate(self.twinkles):
                twinkle['fixture'].setChannels(self.hsv_to_rgb(self.hue, self.saturation, twinkle['value']))
                twinkle['value'] *= .9

                if twinkle['value'] <= target:
                    toDelete.append(index)
            
            for index in reversed(toDelete):
                self.twinkles[index]['fixture'].setChannels(baseColor)
                del self.twinkles[index]

            time.sleep(.01)

        for f in self.fixtures:
            f.setChannels({'red':0,'green':0,'blue':0})
        self.endEvent.set()
    def hsv_to_rgb(self, h, s, v):
        color = colorsys.hsv_to_rgb(h, s, v)
        return {x:int(y * 255) for x,y in zip(['red', 'green', 'blue'], color)}
        
