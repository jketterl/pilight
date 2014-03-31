'''
Created on 01.11.2012

@author: jakob
'''

class FixtureList(list):
    def filter(self, predicate):
        result = FixtureList()
        for fixture in self:
            if (predicate(fixture)): result.append(fixture)
        return result
    def getChannels(self, name):
        result = []
        for fixture in self:
             result.append(fixture.getNamedChannel(name))
        return result

class Manager(object):
    def __init__(self):
        self.fixtures = FixtureList()
    def addFixture(self, fixture):
        self.fixtures.append(fixture)
    def filter(self, predicate):
        return self.fixtures.filter(predicate)
    

FixtureManager = Manager()

class Fixture(object):
    def __init__(self):
        self.tags = []
        FixtureManager.addFixture(self)
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
    def getTags(self):
        return self.tags
    def addTag(self, tag):
        if tag in self.tags: return
        self.tags.append(tag)
    def addTags(self, tags):
        for tag in tags: self.addTag(tag)
    def hasTag(self, *args):
        for tag in args:
            if not tag in self.tags: return False
        return True
    
class Dimmer(Fixture):
    def getInputs(self):
        return ['brightness'];

class RGBFixture(Fixture):
    def __init__(self, channelSequence = 'GRB'):
        self.channelSequence = channelSequence
        super(RGBFixture, self).__init__()
        self.addTag('rgb')
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
