import sys
sys.path.append('../vendors/usbdmx/')

from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import FixtureManager, RGBFixture, StairvillePAR
from module import SubMaster
from filter import AlphaFilter
from show import ShowManager

if __name__ == '__main__':
    subMaster = SubMaster(['red', 'green', 'blue'], 3)
    universe = Universe()
    output = Output.factory('WS2801Output', channels=150)
    output.addFilter(AlphaFilter())
    universe.setOutput(output)
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['ws2801', 'pixel'])

    universe = Universe()
    universe.setOutput(Output.factory('DEOutput', '0000000000001337'))
    for i in range(2):
        fixture = StairvillePAR()
        fixture.mapToUniverse(universe, i * 5)
        fixture.addTags(['dmx'])

    for i in reversed(range(2)):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 10 + 19)
        fixture.addTags(['dmx', 'par'])

    for i in reversed(range(50)):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3 + 49)
        fixture.addTags(['ws2801', 'pixel'])

    for fixture in FixtureManager.filter(lambda f : f.hasTag('rgb')):
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))

    showManager = ShowManager()

    #showManager.addShow('knightrider', 'Knight Rider', [
    #    'KnightRider',
    #    {'red':255, 'green':0, 'blue':0},
    #    {'red':0,   'green':0, 'blue':0}
    #])

    def pixelFilter(f):
        return f.hasTag('pixel')

    def parFilter(f):
        return f.hasTag('par')

    showManager.addShow('snowpixel', 'Snow @ Pixel', ['Snow'], filter = pixelFilter)
    showManager.addShow('snowpar', 'Snow @ Par', ['Snow'], filter = parFilter)
    showManager.addShow('colorfaderpixel', 'Color Fader @ Pixel', ['ColorFader'], filter = pixelFilter)
    showManager.addShow('colorwheelpixel', 'Color Wheel @ Pixel', ['ColorWheel'], filter = pixelFilter)
    showManager.addShow('strobe', 'Strobe @ Pixel', ['Strobe'], filter = pixelFilter)
    #showManager.addShow('vu', 'VU Meter', ['VUMeter', 'hw:1,0'])
    #showManager.addShow('fft', 'FFT Show', ['FFT'])
    showManager.addShow('bpmstrobe', 'BPM Strobe @ Pixel', ['BPMStrobe'], filter = pixelFilter)
    showManager.addShow('police', 'Police @ Pixel', ['Police'], filter = pixelFilter)
    showManager.addShow('twinklepixel', 'Twinkle @ Pixel', ['Twinkle'], filter = pixelFilter)
    showManager.addShow('twinklepar', 'Twinkle @ Par', ['Twinkle'], filter = parFilter)
    showManager.addShow('lichterkettepixel', 'Lichterkette @ Pixel', ['Lichterkette'], filter = pixelFilter)
    showManager.addShow('lichterkettepar', 'Lichterkette @ Par', ['Lichterkette'], filter = parFilter)

    showManager.startShow('colorfaderpixel')
    showManager.startShow('lichterkettepar')
