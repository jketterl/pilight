'''
Created on 16.11.2012

@author: jakob
'''

from .ThreadedOutput import ThreadedOutput
from .ThreadedOutput import WriterThread

class BufferedWriter(WriterThread):
    timeout = 10

class BufferedOutput(ThreadedOutput):
    writerCls = BufferedWriter
    def __init__(self, channels):
        self.buffer = [0] * channels
        super(BufferedOutput, self).__init__()

    def applyChanges(self, changes):    
        for num in changes:
            self.buffer[num] = changes[num]
        self.write()
        
    def write(self):
        pass
