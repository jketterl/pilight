from . import Show
import time

class Wakelight(Show):
    time = 15 * 60 # target time: 15 minutes
    def run(self):
        startTime = time.time()
        elapsed = 0
        while self.doRun and elapsed < self.time:
            elapsed = time.time() - startTime
            color = {
                "red"   : int((float(elapsed) / self.time) * 255)
            }
            green = self.time / 3
            if (elapsed > green): color['green'] = int(float(elapsed - green) / (self.time - green) * 255)

            blue = green * 2
            if (elapsed > blue): color['blue'] = int(float(elapsed - blue) / (self.time - blue) * 255)
            for f in self.fixtures:
                f.setChannels(color)
            time.sleep(.1)

        while self.doRun:
            time.sleep(1)

        for f in self.fixtures:
            f.setChannels({"red":0, "green":0, "blue":0})

        self.endEvent.set()
