from .ThreadedOutput import ThreadedOutput
import socket, threading, re, json, struct

class SocketClient(threading.Thread):
    def __init__(self, sock, server):
        self.socket = sock
        self.server = server
        super(SocketClient, self).__init__()
    def run(self):
        message = self.socket.recv(4096)
        rx = re.compile('^REQUEST (.*)$')
        m = rx.match(message)
        if m is None: return self.socket.close()
        self.server.registerClient(self, m.group(1))
    def sendChanges(self, changes):
        message = ''
        for key in changes:
            message += struct.pack('HB', key, changes[key])
        self.socket.send(message)

class SocketServer(threading.Thread):
    _instance = None
    @staticmethod
    def getInstance():
        if SocketServer._instance is None:
            SocketServer._instance = SocketServer()
        return SocketServer._instance

    def __init__(self):
        super(SocketServer, self).__init__()
        self.clients = {}
        self.start()

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 9191))
        self.server.listen(5)
        while True:
            (client, address) = self.server.accept()
            cm = SocketClient(client, self)
            cm.start()

    def write(self, name, changes):
        if not name in self.clients: return
        self.clients[name].sendChanges(changes)

    def registerClient(self, client, name):
        self.clients[name] = client
        

class SocketOutput(ThreadedOutput):
    def __init__(self, outputId):
        self.outputId = outputId
        SocketServer.getInstance()
        super(SocketOutput, self).__init__()
    def applyChanges(self, changes):
        SocketServer.getInstance().write(self.outputId, changes)
