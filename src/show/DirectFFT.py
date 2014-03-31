from .FFT import FFT

class DirectFFT(FFT):
    def __init__(self, bands, *args, **kwargs):
        super(DirectFFT, self).__init__(bands, *args, **kwargs)
        self.bands = 12
        self.colorConfig = {
            'brightness' : { 'start' : 0, 'end' : 1}
        }
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        self.fixtures[index].setChannels({'brightness':value})
