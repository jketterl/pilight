'''
Created on 01.11.2012

@author: jakob
'''
class Channel(object):
    def __init__(self):
        self.listeners = []
        self.value = 0
        
    def addListener(self, listener):
        self.listeners.append(listener)
        
    def removeListener(self, listener):
        self.listeners.remove(listener)
        
    def setValue(self, value):
        value = max(min(value, 255), 0)
        if self.value == value: return
        self.value = value
        for listener in self.listeners:
            listener.onValueChange(self, value)
            
    def getValue(self):
        return self.value

class ChannelMapping(object):
    def __init__(self, source, target):
        source.addListener(self)
        self.source = source
        self.target = target
    def onValueChange(self, source, value):
        if source is not self.source: return
        self.target.setValue(value)
