from . import Show
import random, threading, time

class SnowDecayThread(threading.Thread):
    def __init__(self, show):
        self.show = show
        self.doRun = True
        self.event = threading.Event()
        super(SnowDecayThread, self).__init__()
    def run(self):
        while self.doRun:
            self.show.decay()
            self.event.wait(.02)
    def stop(self):
        self.doRun = False
        self.event.set()

class Snow(Show):
    def run(self):
        self.lock = threading.Lock()
        self.flakes = {}
        self.fixtures = self.fixtureList.filter(lambda f : f.hasTag('rgb'))
        decayer = SnowDecayThread(self)
        decayer.start()

        while(self.doRun):
            self.lock.acquire()
            channel = random.randint(0, len(self.fixtures) - 1) 
            self.flakes[channel] = 255
            self.fixtures[channel].setChannels(dict(zip(['red', 'green', 'blue'], [255] * 3)))
            self.lock.release()
            time.sleep(random.random() * .4)
            
        decayer.stop()
        for channel in self.flakes:
            self.fixtures[channel].setChannels({'red':0,'green':0,'blue':0})
        self.endEvent.set()

    def decay(self):
        toDelete = []
        self.lock.acquire()
        for channel in self.flakes:
            value = self.flakes[channel]
            value -= 4
            if value <= 0:
                value = 0
                toDelete.append(channel)
            else:
                self.flakes[channel] = value
            self.fixtures[channel].setChannels(dict(zip(['red', 'green', 'blue'], [value] * 3)))
        for channel in toDelete: del self.flakes[channel]
        self.lock.release()
