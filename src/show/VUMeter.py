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
            if self.current != self.target:
                self.set(self.current + (self.target - self.current) / self.smoothingFactor)
            time.sleep(.02)
    def update(self, value):
        self.target = value
    def stop(self):
        self.doRun = False
    def set(self, value):
        self.current = value
        self.output.setValue(value)

class VUOutput(object):
    def __init__(self, fixtures):
        self.fixtures = fixtures;
        count = len(fixtures)
        yellow = count * .7
        red = count * .95
        self.colorMap = [0] * count
        self.value = 0
        for i in range(count):
            if (i < yellow):
                colors = ['green']
            elif (i < red):
                colors = ['green', 'red']
            else:
                colors = ['red']
                
            self.colorMap[i] = dict(zip(colors, [255] * len(colors)))
            
        self.smoother = SmoothingThread(self)
        self.smoother.start()
            
    def update(self, value):
        self.smoother.update(value)
    
    def setValue(self, value):
        value = int(round(value * len(self.fixtures)))
        if (value > self.value):
            for index in range(self.value, value):
                self.fixtures[index].setChannels(self.colorMap[index])
        else:
            for index in range(value, self.value):
                self.fixtures[index].setChannels({'red':0,'green':0,'blue':0})
        self.value = value

    def stop(self):
        self.smoother.stop()
        self.setValue(0)

class VUMeter(Show):
    def __init__(self, fixtures, card = 'hw:0,0'):
        self.card = card
        super(VUMeter, self).__init__(fixtures)
    def run(self):
        lo = 4000
        hi = 32000
        log_lo = math.log(lo)
        log_hi = math.log(hi)
        
        output = VUOutput(self.fixtures)

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
