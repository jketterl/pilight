import sys
sys.path.append('../vendors/usbdmx/')

from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import FixtureManager, RGBFixture, StairvillePAR
from module import SubMaster
from filter import AlphaFilter
from show import ShowManager, ShowFaderMapping, ShowButtonMapping
from channel import ChannelMapping
from net import UDPReceiver, RemoteServer, Bank

if __name__ == '__main__':
    receiver = UDPReceiver()
    receiver.start()

    remoteServer = RemoteServer()
    remoteServer.start()

    subMaster = SubMaster(['red', 'green', 'blue'], 3)
    universe = Universe()
    output = Output.factory('WS2801Output', channels=300)
    output.addFilter(AlphaFilter())
    universe.setOutput(output)
    for i in range(100):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['ws2801', 'pixel'])

    universe = Universe()
    universe.setOutput(Output.factory('DEOutput', '0000000000001337'))
    for i in range(100):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3 + 99)
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
    #showManager.addShow('snowpar', 'Snow @ Par', ['Snow'], filter = parFilter)
    showManager.addShow('colorfaderpixel', 'Color Fader @ Pixel', ['ColorFader'], filter = pixelFilter)
    showManager.addShow('colorwheelpixel', 'Color Wheel @ Pixel', ['ColorWheel'], filter = pixelFilter)
    #showManager.addShow('colorwheelpar', 'Color Wheel @ Par', ['ColorWheel'], filter = parFilter)
    showManager.addShow('strobe', 'Strobe @ Pixel', ['Strobe'], filter = pixelFilter)
    #showManager.addShow('vu', 'VU Meter', ['VUMeter', 'hw:1,0'])
    #showManager.addShow('fft', 'FFT Show', ['FFT'])
    showManager.addShow('bpmstrobe', 'BPM Strobe @ Pixel', ['BPMStrobe'], filter = pixelFilter)
    showManager.addShow('police', 'Police @ Pixel', ['Police'], filter = pixelFilter)
    showManager.addShow('twinklepixel', 'Twinkle @ Pixel', ['Twinkle'], filter = pixelFilter)
    #showManager.addShow('twinklepar', 'Twinkle @ Par', ['Twinkle'], filter = parFilter)
    showManager.addShow('lichterkettepixel', 'Lichterkette @ Pixel', ['Lichterkette'], filter = pixelFilter)
    #showManager.addShow('lichterkettepar', 'Lichterkette @ Par', ['Lichterkette'], filter = parFilter)

    bank = Bank("default")
    ShowFaderMapping(showManager, 'colorwheelpixel', {
        'value': bank.universe[1],
        'saturation': bank.universe[3],
        'speed': bank.universe[5]
    })
    ShowFaderMapping(showManager, 'lichterkettepixel', {'brightness': bank.universe[7]})
    ChannelMapping(bank.universe[0], subMaster.getChannel('red'))
    ChannelMapping(bank.universe[2], subMaster.getChannel('green'))
    ChannelMapping(bank.universe[4], subMaster.getChannel('blue'))
    ShowButtonMapping(bank.universe[8], showManager, 'colorfaderpixel')
    ShowButtonMapping(bank.universe[9], showManager, 'snowpixel')
    ShowButtonMapping(bank.universe[10], showManager, 'twinklepixel')
    ShowButtonMapping(bank.universe[11], showManager, 'bpmstrobe')
    ShowButtonMapping(bank.universe[12], showManager, 'police')
    remoteServer.addBank(bank)

    showManager.startShow('colorfaderpixel')
    #showManager.startShow('lichterkettepar')
