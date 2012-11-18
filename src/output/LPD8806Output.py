'''
Created on 16.11.2012

@author: jakob
'''

from . import BufferedOutput

class LPD8806Output(BufferedOutput):
    def __init__(self, channels, device="/dev/spidev0.0"):
        self.spidev = file(device, "wb")
        super(LPD8806Output, self).__init__(channels)
    
    def write(self):
        output = bytearray(len(self.buffer) + 3)
        for i in range(len(self.buffer)):
            output[i] = 0x80 | int(round(self.buffer[i] / 2))
        self.spidev.write(output)
        self.spidev.flush()
