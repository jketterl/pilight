'''
Created on 16.11.2012

@author: jakob
'''

from . import Output
from threading import Thread, Event, Lock

class WriterThread(Thread):
    def __init__(self, output):
        super(WriterThread, self).__init__();
        self.event = Event()
        self.doStop = False
        self.output = output
    
    def run(self):
        while not self.doStop:
            self.event.wait(10)
            self.event.clear()
            self.output.update()
    
    def stop(self):
        self.doStop = True
        self.intterrupt()
        
    def interrupt(self):
        if self.event.isSet(): return
        self.event.set()
        
class ThreadedOutput(Output):
    def __init__(self):
        self.thread = WriterThread(self)
        self.thread.start()
        super(ThreadedOutput, self).__init__()
        self.changes = {}
        self.changesLock = Lock()
        
    def _setChannelValue(self, channel, value):
        self.changesLock.acquire(True)
        self.changes[channel] = value
        self.changesLock.release()
        self.thread.interrupt()
        
    def update(self):
        self.changesLock.acquire(True)
        changes = self.changes
        self.changes = {}
        self.changesLock.release()
        self.applyChanges(changes)
        
    def applyChanges(self, changes):
        pass
