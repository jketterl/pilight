import threading

class Show(threading.Thread):
    def __init__(self):
        self.endEvent = threading.Event()
        super(Show, self).__init__();
    def waitForEnd(self):
        while not self.endEvent.is_set():
            self.endEvent.wait(60)
        
