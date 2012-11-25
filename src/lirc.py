import socket, re, threading

class LircDelegate(object):
    def onKey(self, remote, key):
        pass

class LircClient(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        super(LircClient, self).__init__()
        # autostart
        self.start()

    def run(self):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect('/var/run/lirc/lircd')

        regex = re.compile('^([0-9a-f]{16}) ([0-9a-f]{2}) ([^ ]+) (.+)\n$')

        while True:
            message = client.recv(4096)

            # parse the message
            match = regex.match(message)
            if match is None: continue

            if match.group(2) != '00': continue

            self.delegate.onKey(match.group(3), match.group(2))
