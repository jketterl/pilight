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
            channel.index = i
            channel.addListener(self)
            self.channels[i] = channel;
        self.output = Output()
        self.filters = []
            
    def __getitem__(self, index):
        return self.channels[index]

    def __setitem__(self, key, value):
        self.channels[key] = value

    def __len__(self):
        return len(self.channels)
    
    def onValueChange(self, source, value):
        for filter in self.filters:
            value = filter.filter(value)
        self.getOutput().setChannel(self.channelIndex(source), value)

    def channelIndex(self, channel):
        return channel.index
        
    def getOutput(self):
        return self.output
    
    def setOutput(self, output):
        self.output = output
        return self

    def addFilter(self, filter):
        self.filters.append(filter)
        return self
