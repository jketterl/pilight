from . import Show
from audio import FFTReader, AudioReader
from universe import Universe
import time

class FFT(Show):
    def run(self):
        self.universe = Universe(16)
        self.reader = FFTReader(AudioReader.instance("hw:1,0"), self.universe, 16)
        for channel in self.universe:
            channel.addListener(self)
        self.reader.start()
        self.endEvent.wait()
    def onValueChange(self, channel, value):
        self.fixtures[self.universe.channelIndex(channel)].setChannels({'blue':value})
    def stop(self):
        self.reader.stop()
        self.reader.endEvent.wait()
        for fixture in self.fixtures:
            fixture.setChannels({'blue':0})
        self.endEvent.set()
        super(FFT, self).stop()
