from .FFT import FFT

class DirectFFT(FFT):
    def __init__(self, fixtures, bands, *args, **kwargs):
        super(DirectFFT, self).__init__(bands, *args, **kwargs)
        self.bands = 16
        #self.fixtures = bands
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        #channels = ['red', 'green', 'blue']
        #self.fixtures[int(index / 3)].setChannels({channels[index % 3]:value})
        #print index
        self.fixtures[index].setChannels({'brightness':value})
