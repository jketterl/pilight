from .FFT import FFT
from fixture import FixtureManager

class DirectFFT(FFT):
    def __init__(self, bands, *args, **kwargs):
        super(DirectFFT, self).__init__(*args, **kwargs)

        # bands contains number of bands in parent
        self.bands = len(bands)
        # so we have to store this somewhere else
        self.b = bands
    def getFixtures(self):
        return FixtureManager.filter(lambda f : f.hasTag('dmx'))
    def onValueChange(self, channel, value):
        index = self.universe.channelIndex(channel)
        self.b[index].setValue(value)
