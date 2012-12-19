'''
Created on 19.12.2012

@author: jakob
'''

from universe import Universe
from channel import Channel, ChannelMapping

class SubMaster(Universe):
    def __init__(self, channelNames = [], count = 512):
        super(SubMaster, self).__init__(count)
        master = Channel()
        self.channelMap = {}
        for index, name in enumerate(channelNames):
            channel = self[index]
            self.channelMap[name] = channel 
            ChannelMapping(master, channel)
        self.channelMap['master'] = master
    def selectChannel(self, channel, fixtures):
        self.currentChannel = self.getChannel(channel)
    def getChannel(self, name):
        return self.channelMap[name]
    def increaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() + 10)
    def decreaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() - 10)
    def mapChannel(self, name, target):
        ChannelMapping(self.getChannel(name), target)