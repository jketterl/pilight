from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import RGBFixture
from module import SubMaster
from filter import AlphaFilter
from show import ShowManager

if __name__ == '__main__':
    fixtures = []

    subMaster = SubMaster(['red', 'green', 'blue'], 3)
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

    showManager = ShowManager(fixtures)

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
    showManager.addShow('twinke', 'Twinkle', ['Twinkle'])

