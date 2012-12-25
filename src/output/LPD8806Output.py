'''
Created on 16.11.2012

@author: jakob
'''

from .BufferedOutput import BufferedOutput

class LPD8806Output(BufferedOutput):
    def __init__(self, channels, device="/dev/spidev0.0"):
        self.spidev = file(device, "wb")
        super(LPD8806Output, self).__init__(channels)
    
    def write(self):
        output = bytearray()
        for i in self.buffer:
            output.append(0x80 | i / 2)
        for i in range(3): output.append(0x00)
        self.spidev.write(output)
        self.spidev.flush()
