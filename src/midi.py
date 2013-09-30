import threading

class Reader(threading.Thread):
    def __init__(self, input, *args, **kwargs):
        self.fp = open('/dev/midi2', 'r')
        self.input = input
        super(Reader, self).__init__(*args, **kwargs)
    def run(self):
        read = 1
        while (read > 0):
            msg = self.fp.read(3)
            read = len(msg)
            val = ord(msg[2])
            self.input.update(0, val * 2)

class MidiInput(object):
    def __init__(self):
        self.reader = Reader(self)
        self.reader.start()
    def update(self, channel, value):
        pass
