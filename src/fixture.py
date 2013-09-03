'''
Created on 01.11.2012

@author: jakob
'''

class Fixture(object):
    def getInputs(self):
        return []
    def mapToChannels(self, config):
        self.mappings = {}
        for channelName in config:
            self.mappings[channelName] = config[channelName]
    def setChannels(self, values):
        for channelName in values:
            self.getNamedChannel(channelName).setValue(values[channelName]);
    def getNamedChannel(self, name):
        if not self.mappings.has_key(name): 
            raise Exception("named channel %s not found" % name)
        return self.mappings[name]
    def mapToUniverse(self, universe, offset = 0):
        channelMap = {}
        for channelName in self.getInputs():
            channelMap[channelName] = universe[offset]
            offset += 1
        self.mapToChannels(channelMap)
    
class Dimmer(Fixture):
    def getInputs(self):
        return ['brightness'];

class RGBFixture(Fixture):
    def __init__(self, channelSequence = 'GRB'):
        self.channelSequence = channelSequence
    def getInputs(self):
        if (self.channelSequence == 'GRB'):
            return [
                'green',
                'red',
                'blue'
            ]
        elif (self.channelSequence == 'RGB'):
            return [
                'red',
                'green',
                'blue'
            ]
