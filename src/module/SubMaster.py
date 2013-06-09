'''
Created on 19.12.2012

@author: jakob
'''

from universe import Universe
from channel import Channel, MultiChannelMapping
from message import Messenger

class SubMaster(Universe):
    def __init__(self, channelNames = [], count = 512):
        super(SubMaster, self).__init__(count)
        master = Channel()
        masterMap = MultiChannelMapping(master)
        self.channelMap = {}
        self.targetMap = {}
        for index, name in enumerate(channelNames):
            channel = self[index]
            self.channelMap[name] = channel
            self.targetMap[name] = MultiChannelMapping(channel)
            masterMap.addTarget(channel) 
        self.channelMap['master'] = master
        self.selectChannel('master', None)
    def selectChannel(self, channel, fixtures):
        self.currentChannel = self.getChannel(channel)
        Messenger.displayMessage('selected: %s' % channel);
    def getChannel(self, name):
        return self.channelMap[name]
    def increaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() + 10)
    def decreaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() - 10)
    def mapChannel(self, name, target):
        self.targetMap[name].addTarget(target)
    def fullValue(self, *args):
        self.currentChannel.setValue(255);
    def offValue(self, *args):
        self.currentChannel.setValue(0);
