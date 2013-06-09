'''
Created on 16.11.2012

@author: jakob
'''

from .BufferedOutput import BufferedOutput
import time

class WS2801Output(BufferedOutput):
    def __init__(self, channels, device="/dev/spidev0.0"):
        self.spidev = file(device, "wb")
        super(WS2801Output, self).__init__(channels)

        self.buffer = bytearray(channels + 3)
        # initialize buffer with zero values
        for i in range(channels):
            self.buffer[i] = 0x00

    def applyChanges(self, changes):
        for num in changes:
            self.buffer[num] = changes[num]
        self.write()
    
    def write(self):
        self.spidev.write(self.buffer)
        self.spidev.flush()
	time.sleep(0.002)
