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
        if self.value == value: return
        self.value = value
        for listener in self.listeners:
            listener.onValueChange(self, value)
