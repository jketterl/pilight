from . import Show
import time, threading

class Fader(threading.Thread):
    def __init__(self, pattern, callback, interval = 50.7):
        self.pattern = pattern
        self.doRun = True
        self.event = threading.Event()
        self.callback = callback
        self.interval = interval
        super(Fader, self).__init__()
    def run(self):
        self.setColor({})
        step = 0
        while (self.doRun):
            origin = self.color
            target = self.pattern[step]
            
            deltas = {}
            channels = target.keys() + origin.keys()
            for key in channels:
                if not key in origin: origin[key] = 0
                if not key in target: target[key] = origin[key]
                deltas[key] = target[key] - origin[key]

            a = deltas.values()
            maxDelta = max(abs(min(a)), abs(max(a)))
            sleep = max(self.interval / maxDelta, .1)

            start = time.time()
            end = start + self.interval

            while self.doRun and time.time() < end:
                ratio = min((time.time() - start) / self.interval, 1)
                current = {}
                for key in deltas:
                    current[key] = int(round(origin[key] + deltas[key] * ratio))
                self.setColor(current)
                self.event.wait(sleep)

            step += 1
            if step >= len(self.pattern): step = 0

            if self.doRun: self.setColor(target)
            self.event.wait(1)
    def setColor(self, color):
        self.color = color
        self.callback(color)
    def stop(self):
        self.doRun = False
        self.event.set()

class ColorFader(Show):
    def __init__(self, fixtures):
        self.colors = [
            {'red':255},
            {'red':0, 'green':255},
            {'green':0, 'blue':255},
            {'blue':0, 'red':255},
            {'green':255},
            {'red':0},
            {'blue':255},
            {'green':0},
            {'red':255},
            {'blue':0},
            {'green':255, 'blue':255},
            {'green':0},
            {'green':255},
            {'blue':0},
            {'blue':255},
            {'red':0},
            {'red':0, 'green':0, 'blue':0}
        ]

        super(ColorFader, self).__init__(fixtures)

    def run(self):
        def setColor(color):
            for fixture in self.fixtures:
                fixture.setChannels(color)
        fader = Fader(self.colors, setColor)
        fader.start()
        self.endEvent.wait()
        fader.stop()
        setColor({'red':0,'green':0,'blue':0})

    def stop(self):
        self.endEvent.set()
        super(ColorFader, self).stop()
