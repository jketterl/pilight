from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import RGBFixture
from module import ShowRunner, SubMaster
from filter import AlphaFilter

class ShowManager(Controllable):
    def __init__(self, *args, **kwargs):
        super(ShowManager, self).__init__(*args, **kwargs)
        self.runner = ShowRunner()
        self.shows = {}
    def getId(self):
        return 'showmanager'
    def getShows(self):
        res = []
        for id in self.shows:
            res.append({'id':id, 'name':self.shows[id]['name']})
        return res
    def addShow(self, id, name, definition):
        self.shows[id] = {'name':name, 'definition':definition}
    def startShow(self, id=None):
        if id is None: return
        args = self.shows[id]['definition'][:]
        # always pass a list of fixtures as the second parameter
        args.insert(1, fixtures)

        self.runner.startShow(*tuple(args))
    def stopShow(self):
        self.runner.stopCurrentShow()

if __name__ == '__main__':
    fixtures = []

    subMaster = SubMaster(['red', 'green', 'blue'], 3)
    showManager = ShowManager()

    showManager.addShow('knightrider', 'Knight Rider', [
        'KnightRider',
        {'red':255, 'green':0, 'blue':0},
        {'red':0,   'green':0, 'blue':0}
    ])
    showManager.addShow('snow', 'Snow', ['Snow'])
    showManager.addShow('colorfader', 'Color Fader', ['ColorFader'])
    showManager.addShow('colorwheel', 'Color Wheel', ['ColorWheel'])
    showManager.addShow('strobe', 'Strobe', ['Strobe', 20, 30])
    showManager.addShow('vu', 'VU Meter', ['VUMeter', 'hw:1,0'])
    showManager.addShow('fft', 'FFT Show', ['FFT'])
    showManager.addShow('bpmstrobe', 'BPM Strobe', ['BPMStrobe'])
    showManager.addShow('police', 'Police', ['Police'])

    universe = Universe()
    output = Output.factory('WS2801Output', channels=150)
    output.addFilter(AlphaFilter())
    universe.setOutput(output)
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))
