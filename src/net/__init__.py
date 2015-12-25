from threading import Thread
import select, socket, time

from universe import Universe
from output import Output

class UDPReceiver(Thread):
    def run(self):
        self.doRun = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 9000))
        s.setblocking(0)

        while (self.doRun):
            result = select.select([s], [], [])
            msg, src = result[0][0].recvfrom(1024)
            if (msg.rstrip('\0') == 'hello pilight'):
                print "incoming pilight broadcast from " + src[0]

                res = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                res.sendto("hello remote", (src[0], 9001))

    def stop(self):
        self.doRun = False

class Bank:
    def __init__(self, name):
        self.name = name;
        self.faders = Universe(8)
        self.buttons = Universe(8)
        self.leds = Universe(8)

class SocketOutput(Output):
    def __init__(self, distributor, channelCount):
        self.distributor = distributor
        self.values = [0 for i in range(channelCount)]
        super(SocketOutput, self).__init__()
    def _setChannelValue(self, channel, value):
        self.values[channel] = value
        message = bytearray(11)
        message[0:3] = 'LED'
        for i in range(8):
            message[3 + i] = self.values[i]
        self.distributor.distribute(message)


class RemoteServer(Thread):
    def __init__(self):
        self.banks = []
        self.sockets = []
        super(RemoteServer, self).__init__()
    def run(self):
        self.doRun = True

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 9000))
        s.listen(1)

        while (self.doRun):
            conn, addr = s.accept()
            print "new remote connection from ", addr
            remote = RemoteThread(conn, self.banks)
            self.sockets.append(remote)
            remote.start()
    def addBank(self, bank):
        self.banks.append(bank)
        bank.leds.setOutput(SocketOutput(self, 8))
    def distribute(self, message):
        for sock in self.sockets:
            try:
                sock.send(message)
            except socket.error as e:
                print(e)

class RemoteThread(Thread):
    def __init__(self, conn, banks):
        self.conn = conn
        self.banks = banks
        self.bank = 0
        super(RemoteThread, self).__init__()
        self.sendBankName()
    def getCurrentBank(self):
        if (self.bank >= len(self.banks)): return None
        return self.banks[self.bank]
    def run(self):
        self.doRun = True
        buf = bytearray(11)
        view = memoryview(buf)
        while (self.doRun):
            read = self.conn.recv_into(view, 11)
            if (read < 0):
                print "WARN: error receiving on socket"
            if (read >= 11):
                type = buf[0:3]
                bank = self.getCurrentBank()

                if (type == "VAL"):
                    if bank is not None:
                        for i in range(8):
                            bank.faders[i].setValue(buf[i+3])
                elif (type == "BUP"):
                    self.bank = (self.bank + 1) % len(self.banks)
                    self.sendBankName()
                elif (type == "BDN"):
                    self.bank = (self.bank - 1) % len(self.banks)
                    self.sendBankName()
                elif (type == "BUT"):
                    buttons = buf[3]
                    if bank is not None:
                        for i in range(8):
                            bank.buttons[i].setValue(255 if buttons & (1 << i) else 0)
    def send(self, message):
        self.conn.sendall(message)
    def sendBankName(self):
        name = self.getCurrentBank().name
        message = bytearray(4 + len(name))
        message[0:3] = 'BNK'
        message[3] = len(name)
        message[4:] = name
        self.send(message)
