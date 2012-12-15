import threading, math, struct, numpy
from universe import Universe
from output import Output

class FFTReader(threading.Thread):
    def __init__(self, audioreader, universe, bands):
        self.doRun = True
        self.audioreader = audioreader
        self.bands = bands
        self.universe = universe

        self.fftConversion = [0] * self.bands
        ratio = math.log(1023, 2) / self.bands
        start = 1
        for index in range(self.bands):
            end = math.pow(2, (index + 1) * ratio)
            self.fftConversion[index] = [int(start), int(end) + 1]
            start = end

        self.endEvent = threading.Event()

        super(FFTReader, self).__init__()
    def run(self):
        lo = math.log(100000)
        hi = math.log(20000000)
        while (self.doRun):
            self.audioreader.event.wait()

            form = '<%dh' % (self.audioreader.l * 2)
            data = struct.unpack(form, self.audioreader.data)

            fft = numpy.abs(numpy.fft.fft(data))

            #fft = fft[0:len(fft)/2]

            for index, data in enumerate(self.fftConversion):
                power = numpy.amax(fft[data[0]:data[1]])
                power = int(((math.log(power) - lo) / (hi - lo)) * 255)
                self.universe[index].setValue(max(min(power, 255), 0))
        self.endEvent.set()
    def stop(self):
        self.doRun = False

