'''
Created on Nov 19, 2012

@author: jketterl
'''

from . import Show
import time

class KnightRider(Show):
    def __init__(self, fixtures, highval, lowval):
        self.highval = highval
        self.lowval = lowval
        super(KnightRider, self).__init__(fixtures);
        
    def run(self):
        previous = self.fixtures[0]
        while self.doRun:
            for i in range(len(self.fixtures)):
                previous.setChannels(self.lowval)
                previous = self.fixtures[i]
                previous.setChannels(self.highval)
                time.sleep(.01)

            for i in range(len(self.fixtures) - 2, 0, -1):
                previous.setChannels(self.lowval)
                previous = self.fixtures[i]
                previous.setChannels(self.highval)
                time.sleep(.01)
        previous.setChannels(self.lowval)
        
        self.endEvent.set()
