from .BufferedOutput import BufferedOutput
from artnet.packet import *
import socket

class ArtnetOutput(BufferedOutput):
    def __init__(self, target):
        self.target = target
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.connect((target, 6454))
        super(ArtnetOutput, self).__init__(256)
    def write(self):
        packet = DmxPacket()
        for i, value in enumerate(self.buffer):
            packet[i] = value
        self.socket.sendall(packet.encode())
