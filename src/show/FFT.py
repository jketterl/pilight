from . import Show
from audio import FFTReader, AudioReader
from universe import Universe
from .VUMeter import VUOutput

class FFT(Show):
    def run(self):
        bands = 12
        self.universe = Universe(bands)
        for channel in self.universe:
            channel.addListener(self)

        self.outputs = []
        self.ratio = float(len(self.fixtures)) / bands
        start = 0
        for i in range(bands):
            end = int((i+1) * self.ratio)
            self.outputs.append(VUOutput(self.fixtures[start:end]))
            start = end

        self.reader = FFTReader(AudioReader.instance("hw:1,0"), self.universe, bands)
        self.reader.start()
        self.endEvent.wait()
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        value = float(value) / 255 * self.ratio
        self.outputs[index].update(value)
    def stop(self):
        self.reader.stop()
        self.reader.endEvent.wait()
        for output in self.outputs:
            output.stop()
        self.endEvent.set()
        super(FFT, self).stop()
