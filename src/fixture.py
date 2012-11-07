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
    
class RGBFixture(Fixture):
    def getInputs(self):
        return [
            'red',
            'green',
            'blue'
        ]