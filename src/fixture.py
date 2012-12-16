'''
Created on 01.11.2012

@author: jakob
'''

class Fixture(object):
    def getInputs(self):
        return []
    def mapToChannels(self, config):
        self.mappings = {}
        for key in config:
            self.mappings[key] = config[key]
    def setChannels(self, values):
        for key in values:
            self.mappings[key].setValue(values[key]);
    def mapToUniverse(self, universe, offset = 0):
        channelMap = {}
        for channel in self.getInputs():
            channelMap[channel] = universe[offset]
            offset += 1
        self.mapToChannels(channelMap)
    
class RGBFixture(Fixture):
    def getInputs(self):
        return [
            'green',
            'red',
            'blue'
        ]