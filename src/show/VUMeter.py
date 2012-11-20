'''
Created on Nov 19, 2012

@author: jketterl
'''

from . import Show
import alsaaudio, audioop, math, threading, time

class AudioReader(threading.Thread):
    def __init__(self, card):
        self.sound = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
        self.sound.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.sound.setrate(48000)
        self.sound.setchannels(1)
        self.sound.setperiodsize(1024)
        self.data = None
        self.l = -1
        self.event = threading.Event()
        self.doRun = True
        super(AudioReader, self).__init__()
    def run(self):
        while self.doRun:
            self.l, self.data = self.sound.read()
            self.event.set()
    def stop(self):
        self.doRun = False
        
class SmoothingThread(threading.Thread):
    def __init__(self, output):
        self.output = output
        self.doRun = True
        self.current = 0
        self.target = 0
        self.smoothingFactor = 8
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
        output = []
        for index in range(len(self.fixtures)):
            if (index < value):
                output.append(self.colorMap[index])
            else:
                output.append({'red':0,'green':0,'blue':0})
        for fixture in self.fixtures:
            fixture.setChannels(output.pop(0))

class VUMeter(Show):
    def __init__(self, fixtures, card = 'hw:0,0'):
        self.fixtures = fixtures
        self.card = card
        super(VUMeter, self).__init__()
    def run(self):
        lo = 2000
        hi = 32000
        log_lo = math.log(lo)
        log_hi = math.log(hi)
        
        count = len(self.fixtures)
        
        output = VUOutput(self.fixtures)

        audioReader = AudioReader(self.card)
        audioReader.start()
        
        while self.doRun:
            audioReader.event.wait()
            audioReader.event.clear()
            if audioReader.l < 0:
                continue

            vu = (math.log(float(max(audioop.max(audioReader.data, 2), 1))) - log_lo) / (log_hi - log_lo)
            vu = min(max(int(vu * (count + 1)), 0), count)
            
            output.update(vu)

        audioReader.stop()
        output.smoother.stop()
        self.endEvent.set()
