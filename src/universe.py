'''
Created on 01.11.2012

@author: jakob
'''

from channel import Channel
from output import Output

class Universe(object):
    
    def __init__(self, channels = 512):
        self.channels = [None] * channels
        for i in range(0, channels):
            channel = Channel()
            channel.addListener(self)
            self.channels[i] = channel;
        self.output = Output
            
    def __getitem__(self, index):
        return self.channels[index]
    
    def onValueChange(self, source, value):
        self.getOutput().setChannel(self.channels.index(source), value)
        
    def getOutput(self):
        return self.output
    
    def setOutput(self, output):
        self.output = output
        return self