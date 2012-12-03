from . import Input
import threading, socket
from artnet import packet

class ArtnetInput(Input):
    def __init__(self, universe):
        self.universe = universe
        sock = ArtnetSocket(self)
        sock.start()
    def receive(self, p):
        for i in range(min(512, len(self.universe))):
            self.universe[i].setValue(p[i])

class ArtnetSocket(threading.Thread):
    def __init__(self, input):
        self.doRun = True
        self.input = input
        super(ArtnetSocket, self).__init__()
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 6454))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while (self.doRun):
            data, addr = sock.recvfrom(1024)
            p = packet.ArtNetPacket.parse(addr, data)
            if isinstance(p, packet.DmxPacket):
                self.input.receive(p)
