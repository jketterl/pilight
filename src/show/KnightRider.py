'''
Created on Nov 19, 2012

@author: jketterl
'''

from . import Show
import time
from fixture import FixtureManager

class KnightRider(Show):
    def __init__(self, highval, lowval):
        self.highval = highval
        self.lowval = lowval
        super(KnightRider, self).__init__();
        
    def run(self):
        fixtures = FixtureManager.filter(lambda f : f.hasTag('rgb'))
        previous = fixtures[0]
        while self.doRun:
            for i in range(len(fixtures)):
                previous.setChannels(self.lowval)
                previous = fixtures[i]
                previous.setChannels(self.highval)
                time.sleep(.01)

            for i in range(len(fixtures) - 2, 0, -1):
                previous.setChannels(self.lowval)
                previous = fixtures[i]
                previous.setChannels(self.highval)
                time.sleep(.01)
        previous.setChannels(self.lowval)
        
        self.endEvent.set()
