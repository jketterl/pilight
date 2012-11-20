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

        audioReader = AudioReader(self.card)
        audioReader.start()
        
        while self.doRun:
            audioReader.event.wait()
            audioReader.event.clear()
            if audioReader.l < 0:
                continue

            vu = (math.log(float(max(audioop.max(audioReader.data, 2), 1))) - log_lo) / (log_hi - log_lo)
            vu = min(max(int(vu * (len(self.fixtures) + 1)), 0), len(self.fixtures))
            
            for index, fixture in enumerate(self.fixtures):
                if (index < len(self.fixtures) * .7):
                    colors = ['green']
                elif (index < len(self.fixtures) * .95):
                    colors = ['green', 'red']
                else:
                    colors = ['red']
                    
                color = {}
                for c in colors: color[c] = 255
                
                if index < vu:
                    fixture.setChannels(color)
                else:
                    fixture.setChannels({'red':0,'green':0,'blue':0})

        audioReader.stop()            
        self.endEvent.set()
