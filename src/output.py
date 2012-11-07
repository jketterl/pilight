'''
Created on 01.11.2012

@author: jakob
'''

class Output(object):
    def setChannel(self, channel, value):
        pass
    
class ConsoleOutput(Output):
    def setChannel(self, channel, value):
        print 'setting channel %i to %i' % (channel, value)