from threading import Thread
import select, socket, time

from universe import Universe

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
    def __init__(self, name, universe = None):
        if universe is None:
            universe = Universe(16)
        self.name = name;
        self.universe = universe

class RemoteServer(Thread):
    def __init__(self):
        self.banks = []
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
            RemoteThread(conn, self.banks).start()
    def addBank(self, bank):
        self.banks.append(bank)

class RemoteThread(Thread):
    def __init__(self, conn, banks):
        self.conn = conn
        self.banks = banks
        self.bank = 0
        super(RemoteThread, self).__init__()
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
                            bank.universe[i].setValue(buf[i+3])
                elif (type == "BUP"):
                    self.bank = (self.bank + 1) % len(self.banks)
                    print("bank up: " + self.getCurrentBank().name)
                elif (type == "BDN"):
                    self.bank = (self.bank - 1) % len(self.banks)
                    print("bank down: " + self.getCurrentBank().name)
                elif (type == "BUT"):
                    buttons = buf[3]
                    if bank is not None:
                        for i in range(8):
                            bank.universe[8 + i].setValue(255 if buttons & (1 << i) else 0)
