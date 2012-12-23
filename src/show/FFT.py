from . import Show
from audio import FFTReader, AudioReader
from universe import Universe
import time

class FFT(Show):
    def run(self):
        bands = len(self.fixtures)
        self.universe = Universe(bands)
        for i in range(bands):
            self.universe[i] = self.fixtures[i].getNamedChannel('blue');
        self.reader = FFTReader(AudioReader.instance("hw:1,0"), self.universe, bands)
        self.reader.start()
        self.endEvent.wait()
    def stop(self):
        self.reader.stop()
        self.reader.endEvent.wait()
        for fixture in self.fixtures:
            fixture.setChannels({'blue':0})
        self.endEvent.set()
        super(FFT, self).stop()
