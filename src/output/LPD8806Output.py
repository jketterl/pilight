'''
Created on 16.11.2012

@author: jakob
'''

from .BufferedOutput import BufferedOutput

class LPD8806Output(BufferedOutput):
    def __init__(self, channels, device="/dev/spidev0.0"):
        self.spidev = file(device, "wb")
        super(LPD8806Output, self).__init__(channels)

        self.buffer = bytearray(channels + 3)
        # initialize buffer with zero values (for the LPD8806 chip, 0x80 is zero)
        for i in range(channels):
            self.buffer[i] = 0x80

    def applyChanges(self, changes):
        for num in changes:
            self.buffer[num] = (0x80 | changes[num] / 2)
        self.write()
    
    def write(self):
        self.spidev.write(self.buffer)
        self.spidev.flush()
