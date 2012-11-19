'''
Created on Nov 19, 2012

@author: jketterl
'''

from . import Show
import time

class KnightRider(Show):
    def __init__(self, fixtures, highval, lowval):
        self.fixtures = fixtures
        self.highval = highval
        self.lowval = lowval
        super(KnightRider, self).__init__();
        
    def run(self):
        previous = self.fixtures[0]
        for n in range(15):
            for i in range(len(self.fixtures)):
                previous.setChannels({'red':0,'green':0,'blue':0})
                previous = self.fixtures[i]
                previous.setChannels({'red':255,'blue':255,'green':255})
                time.sleep(.01)

            for i in range(len(self.fixtures) - 2, 0, -1):
                previous.setChannels({'red':0,'green':0,'blue':0})
                previous = self.fixtures[i]
                previous.setChannels({'red':255,'blue':255,'green':255})
                time.sleep(.01)
        previous.setChannels({'red':0,'green':0,'blue':0})
        
        self.endEvent.set()