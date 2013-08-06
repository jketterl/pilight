from . import Input
import socket, struct, time

class SocketInput(Input):
    def __init__(self, universe, server, outputId):
        super(SocketInput, self).__init__()
        self.universe = universe
        self.server = server
        self.outputId = outputId
        while True:
            self.run()
            time.sleep(10)
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, 9191))
            self.socket.send('REQUEST %s' % self.outputId)
            data = ''
            while True:
                data += self.socket.recv(4096)
                if len(data) == 0:
                    return
                while len(data) >= 3:
                    (channel, value) = struct.unpack('HB', data[:3])
                    self.universe[channel].setValue(value)
                    data = data[3:]
        except socket.error:
            pass
