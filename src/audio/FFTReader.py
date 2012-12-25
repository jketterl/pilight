import threading, math, struct, numpy
from output import Output

class FFTReader(threading.Thread):
    def __init__(self, audioreader, universe, bands):
        self.doRun = True
        self.audioreader = audioreader
        self.bands = bands

        self.fftConversion = [0] * self.bands
        # reduce frequency range to audible frequencies (854 = ca. 20khz)
        ratio = math.log(854, 2) / self.bands
        start = 1
        for index in range(self.bands):
            end = math.pow(2, (index + 1) * ratio)
            self.fftConversion[index] = (universe[index], int(start), int(end) + 1)
            start = end

        self.endEvent = threading.Event()

        super(FFTReader, self).__init__()
    def run(self):
        lo = math.log(200000)
        hi = math.log(20000000)
        while (self.doRun):
            self.audioreader.event.wait()

            form = '<%dh' % (self.audioreader.l * 2)
            data = struct.unpack(form, self.audioreader.data)

            fft = numpy.abs(numpy.fft.fft(data))

            batch = []
            for (channel, start, end) in self.fftConversion:
                power = numpy.amax(fft[start:end])
                power = int(((math.log(power) - lo) / (hi - lo)) * 255)
                batch.append((channel, max(min(power, 255), 0)))

            for (channel, value) in batch:
                channel.setValue(value)
        self.endEvent.set()
    def stop(self):
        self.doRun = False

