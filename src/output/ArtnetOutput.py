from .BufferedOutput import BufferedOutput
from artnet.packet import *
import socket
import threading
import time
import fcntl, os

class ArtnetBroadcaster(threading.Thread):
    _instance = None
    @staticmethod
    def getInstance():
        if ArtnetBroadcaster._instance is None:
            ArtnetBroadcaster._instance = ArtnetBroadcaster()
        return ArtnetBroadcaster._instance

    def __init__(self):
	super(ArtnetBroadcaster, self).__init__()
        self.knownHosts = [None] * 256
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        fcntl.fcntl(self.socket, fcntl.F_SETFL, os.O_NONBLOCK)
	self.socket.bind(('', 6454))
	self.doRun = True
        self.start()

    def run(self):
        ip_address = socket.gethostbyname(socket.gethostname())
	# TODO get the real broadcast
        broadcast = "192.168.1.255"
	while (self.doRun):
            packet = PollPacket(source=(ip_address, 6454))
            self.socket.sendto(packet.encode(), (broadcast, 6454))
            try:
		while (True):
                    data, addr = self.socket.recvfrom(1024)
                    p = ArtNetPacket.parse(addr, data)
                    if isinstance(p, PollReplyPacket):
                        universe = p.replydata[37]
                        self.knownHosts[universe] = addr
            except socket.error:
                pass
            time.sleep(10)

    def stop(self):
        self.doRun = False

    def getAddr(self, universe):
        try:
            return self.knownHosts[universe]
        except IndexError:
            return None

class ArtnetOutput(BufferedOutput):
    def __init__(self, universe):
        ArtnetBroadcaster.getInstance()
        self.artnetUniverse = universe
        super(ArtnetOutput, self).__init__(512)
    def write(self):
        packet = DmxPacket(universe = self.artnetUniverse)
        for i, value in enumerate(self.buffer):
            packet[i] = value
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            target = ArtnetBroadcaster.getInstance().getAddr(self.artnetUniverse)
            if target is None:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.connect(("192.168.1.255", 6545))
            else:
                s.connect(target)
            s.sendall(packet.encode())
        except socket.error:
            pass
