'''
Created on Nov 21, 2012

@author: jketterl
'''

import threading, time

class BeatDetector(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        self.doRun = True
        self.BPM = 130
        super(BeatDetector, self).__init__()
    def run(self):
        while self.doRun:
            self.delegate.onBeat()
            time.sleep(1.0 / self.BPM * 60)
            pass
    def stop(self):
        self.doRun = False

class BeatDelegate(object):
    def onBeat(self):
        pass