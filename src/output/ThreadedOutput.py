'''
Created on 16.11.2012

@author: jakob
'''

from . import Output
from threading import Thread, Event

class WriterThread(Thread):
    def __init__(self, output):
        super(WriterThread, self).__init__();
        self.event = Event()
        self.doStop = False
        self.output = output
    
    def run(self):
        while not self.doStop:
            self.event.wait(60)
            if self.event.isSet():
                self.event.clear()
            self.output.update()
    
    def stop(self):
        self.doStop = True
        self.intterrupt()
        
    def interrupt(self):
        self.event.set()
        
class ThreadedOutput(Output):
    def __init__(self):
        self.thread = WriterThread(self)
        self.thread.start()
        super(ThreadedOutput, self).__init__()
        self.changes = None
        
    def setChannel(self, channel, value):
        if self.changes is None:
            self.changes = {channel:value}
        else:
            self.changes[channel] = value
        self.thread.interrupt()
        
    def update(self):
        changes = self.changes
        self.changes = None
        self.applyChanges(changes)
        
    def applyChanges(self, changes):
        pass