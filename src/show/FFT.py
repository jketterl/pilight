from . import Show
from audio import FFTReader, AudioReader
from universe import Universe
from .VUMeter import VUOutput

class FFT(Show):
    def __init__(self, *args, **kwargs):
        self.bands = 12
        super(FFT, self).__init__(*args, **kwargs)
    def run(self):
        self.universe = Universe(self.bands)
        for channel in self.universe:
            channel.addListener(self)

        self.outputs = []
        self.ratio = float(len(self.fixtures)) / self.bands
        start = 0
        colorConfig = {
            'blue':{
                'start':0,
                'end':.8
            },
            'red':{
                'start':.8,
                'end':1
            }
        }
        for i in range(self.bands):
            end = int((i+1) * self.ratio)
            self.outputs.append(VUOutput(self.fixtures[start:end], colorConfig))
            start = end

        self.reader = FFTReader(AudioReader.instance("hw:1,0"), self.universe, self.bands)
        self.reader.start()
        self.endEvent.wait()
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        value = float(value) / 255
        self.outputs[index].update(value)
    def stop(self):
        self.reader.stop()
        self.reader.endEvent.wait()
        for output in self.outputs:
            output.stop()
        self.endEvent.set()
        super(FFT, self).stop()

