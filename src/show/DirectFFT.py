from .FFT import FFT

class DirectFFT(FFT):
    def __init__(self, fixtures, bands, *args, **kwargs):
        super(DirectFFT, self).__init__(bands, *args, **kwargs)
        self.bands = 16
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        self.fixtures[index].setChannels({'brightness':value})
    def stop(self):
        self.reader.stop()
        self.reader.endEvent.wait()
        for f in self.fixtures:
            f.setChannels({'brightness':0});
        self.endEvent.set()
        super(FFT, self).stop()

