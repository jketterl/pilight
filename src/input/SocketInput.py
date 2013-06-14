from . import Input
import socket, struct

class SocketInput(Input):
	def __init__(self, universe, server, outputId):
		self.universe = universe
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((server, 9191))
		self.socket.send('REQUEST %s' % outputId)
		data = ''
		while 1:
			data += self.socket.recv(4096)
			while len(data) >= 3:
				(channel, value) = struct.unpack('HB', data[:3])
				self.universe[channel].setValue(value)
				data = data[3:]
		super(SocketInput, self).__init__()
