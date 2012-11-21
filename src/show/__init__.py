import threading

class Show(threading.Thread):
    def __init__(self):
        self.endEvent = threading.Event()
        self.doRun = True
        super(Show, self).__init__();
    def stop(self):
        self.doRun = False
    def waitForEnd(self):
        while not self.endEvent.is_set():
            self.endEvent.wait(60)
        