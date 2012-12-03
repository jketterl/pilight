from . import Input
import threading, socket
from artnet import packet

print Input

class ArtnetInput(Input):
    def __init__(self):
        sock = ArtnetSocket()
        sock.start()

class ArtnetSocket(threading.Thread):
    def __init__(self):
        self.doRun = True
        super(ArtnetSocket, self).__init__()
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 6454))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while (self.doRun):
            data, addr = sock.recvfrom(1024)
            p = packet.ArtNetPacket.parse(addr, data)
            print p
