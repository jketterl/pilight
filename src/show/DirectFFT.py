from .FFT import FFT
from fixture import FixtureManager

class DirectFFT(FFT):
    def __init__(self, bands, *args, **kwargs):
        super(DirectFFT, self).__init__(*args, **kwargs)
        self.bands = 6
        self.colorConfig = {
            'brightness' : { 'start' : 0, 'end' : 1}
        }
        self.fixtures = self.getFixtures()
    def getFixtures(self):
        return FixtureManager.filter(lambda f : f.hasTag('dmx'))
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        self.fixtures[index].setChannels({'brightness':value})
