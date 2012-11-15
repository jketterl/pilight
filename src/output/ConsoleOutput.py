'''
Created on 15.11.2012

@author: jakob
'''
from . import Output

class ConsoleOutput(Output):
    def setChannel(self, channel, value):
        print 'setting channel %i to %i' % (channel, value)