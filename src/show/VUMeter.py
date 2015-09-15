'''
Created on Nov 19, 2012

@author: jketterl
'''

from . import Show
from audio import AudioReader
import audioop, math, threading, time

class SmoothingThread(threading.Thread):
    def __init__(self, output):
        self.output = output
        self.doRun = True
        self.current = float(0)
        self.target = 0
        self.smoothingFactor = float(4)
        super(SmoothingThread, self).__init__()
    def run(self):
        while(self.doRun):
            if self.current > self.target:
                self.set(self.current + (self.target - self.current) / self.smoothingFactor)
            elif self.current < self.target:
                self.set(self.target)
            time.sleep(.02)
    def update(self, value):
        self.target = value
    def stop(self):
        self.doRun = False
    def set(self, value):
        self.current = value
        self.output.setValue(value)

class VUOutput(object):
    def __init__(self, fixtures, colorConfig = None):
        self.fixtures = fixtures;
        if colorConfig is None: colorConfig = {
            'green':{
                'start':0,
                'end':.95
            },
            'red':{
                'start':.7,
                'end':1
            }
        }
        self.len = len(fixtures)
        self.colorMap = [0] * self.len
        self.value = 0
        for i in range(self.len):
            res = {}
            for color in colorConfig:
                entry = colorConfig[color]
                if i >= entry['start'] * self.len and i < entry['end'] * self.len:
                    res[color] = 255
                else:
                    res[color] = 0

            self.colorMap[i] = res
        self.smoother = SmoothingThread(self)
        self.smoother.start()
            
    def update(self, value):
        self.smoother.update(value)
    
    def setValue(self, value):
        if value > 1: print "alert"
        v = value * self.len
        r = v % 1
        value = int(v)

        #print "new values: ", value, int(r * 255)

        if (v > self.value):
            #print "setting: ", int(self.value), value
            for index in range(int(self.value), value):
                self.fixtures[index].setChannels(self.colorMap[index])
        else:
            #print "unsetting: ", value + 1, int(self.value) + 1
            for index in range(value + 1, min(int(self.value) + 1, self.len)):
                self.fixtures[index].setChannels({'red':0,'green':0,'blue':0})
        if value < self.len:
            x = self.colorMap[value].copy()
            for k in x:
                x[k] = int(round(x[k] * r))
            #print "half-tone:", value, x
            self.fixtures[value].setChannels(x)
        self.value = v

    def stop(self):
        self.smoother.stop()
        self.setValue(0)

class VUMeter(Show):
    def __init__(self, card = 'hw:0,0', filter = None):
        self.card = card
        super(VUMeter, self).__init__()
    def run(self):
        lo = 4000
        hi = 32000
        log_lo = math.log(lo)
        log_hi = math.log(hi)
        fixtures = self.fixtureList.filter(lambda f : f.hasTag('strip'))
        
        output = VUOutput(fixtures)

        audioReader = AudioReader.instance(self.card)
        #audioReader.start()
        
        while self.doRun:
            audioReader.event.wait()

            vu = (math.log(float(max(audioop.max(audioReader.data, 2), 1))) - log_lo) / (log_hi - log_lo)
            vu = min(max(vu, 0), 1)
            
            output.update(vu)

        #audioReader.stop()
        output.stop()
        self.endEvent.set()
