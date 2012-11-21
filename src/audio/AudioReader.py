'''
Created on Nov 21, 2012

@author: jketterl
'''

import alsaaudio, threading

class AudioReader(threading.Thread):
    def __init__(self, card='hw:0,0'):
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
