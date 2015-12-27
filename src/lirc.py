import socket, re, threading, os, select

class LircDelegate(object):
    def onKey(self, remote, key):
        pass

class LircClient(threading.Thread):
    def __init__(self, delegate):
        self.delegate = delegate
        super(LircClient, self).__init__()
        # autostart
        self.doRun = True
        self.start()

    def stop(self):
        self.doRun = False
        os.write(self.interruptPipe[1], 'x')

    def run(self):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect('/var/run/lirc/lircd')

        self.interruptPipe = os.pipe()

        regex = re.compile('^([0-9a-f]{16}) ([0-9a-f]{2}) ([^ ]+) (.+)\n$')

        while self.doRun:
            res = select.select([client, self.interruptPipe[0]], [], [])
            if (res[0][0] == client):
                message = client.recv(4096)

                # parse the message
                match = regex.match(message)
                if match is None: continue

                if match.group(2) != '00': continue

                self.delegate.onKey(match.group(3), match.group(2))
