'''
Created on 01.11.2012

@author: jakob
'''

import sys
sys.path.append('../vendors/python-artnet/src/')
sys.path.append('../vendors/adafruit/Adafruit_PWM_Servo_Driver/')
sys.path.append('../vendors/usbdmx/')

from universe import Universe
from filter import AlphaFilter
from fixture import RGBFixture, Dimmer, FixtureManager, StairvillePAR
from output import Output
import time
from lirc import *
from module import SubMaster
from show import ShowManager

from message import Messenger
from message.output import ConsoleOutput, LCDOutput, Messaging

from midi import MidiInput

from alert import Alert
import datetime

class LightWake(Alert):
    def __init__(self, manager):
        print "initializing light wake"
        self.manager = manager
        super(LightWake, self).__init__(datetime.time(06, 45))
    def run(self):
        print "starting wakeup light show"
        self.manager.startShow('wakelight')

'''
class WsListener(WebsocketListener):
    def __init__(self, lirc):
        self.lirc = lirc
    def receive(self, message):
        self.lirc.onKey(message, None)
'''

class MidiBridge(MidiInput):
    def __init__(self, subMaster):
        self.subMaster = subMaster
        super(MidiBridge, self).__init__()
    def update(self, channel, value):
        if channel != 0: return
        self.subMaster.setChannelValue('dj', value)

class LircListener(LircDelegate):
    _showMappings = [
        {
            'keys':['1'],
            'module':'showManager',
            'method':'startShow',
            'args':['vu']
        },
        {
            'keys':['2'],
            'module':'showManager',
            'method':'startShow',
            'args':['knightrider']
        },
        {
            'keys':['3'],
            'module':'showManager',
            'method':'startShow',
            'args':['police']
        },
        {
            'keys':['4'],
            'module':'showManager',
            'method':'startShow',
            'args':['snow']
        },
        {
            'keys':['5'],
            'module':'showManager',
            'method':'startShow',
            'args':['colorfader']
        },
        {
            'keys':['6'],
            'module':'showManager',
            'method':'startShow',
            'args':['colorwheel']
        },
        {
            'keys':['7'],
            'module':'showManager',
            'method':'startShow',
            'args':['fft']
        },
        {
            'keys':['8'],
            'module':'showManager',
            'method':'startShow',
            'args':['bpmstrobe']
        },
        {
            'keys':['9'],
            'module':'showManager',
            'method':'startShow',
            'args':['strobe']
        },
        {
            'keys':['stop','standby'],
            'module':'showManager',
            'method':'stopAllShows'
        },
        {
            'keys':['red','R'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['master red']
        },                     
        {
            'keys':['green','G'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['master green']
        },                     
        {
            'keys':['blue','B'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['master blue']
        },                     
        {
            'keys':['yellow'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['dj']
        },
        {
            'keys':['txt','M'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['master']
        },
        {
            'keys':['chan+','U'],
            'module':'subMaster',
            'method':'increaseValue'
        },
        {
            'keys':['chan-','D'],
            'module':'subMaster',
            'method':'decreaseValue'
        },
        {
            'keys':['vol-'],
            'module':'subMaster',
            'method':'fullValue'
        },
        {
            'keys':['mute'],
            'module':'subMaster',
            'method':'offValue'
        }
    ]
    def __init__(self, modules):
        self.modules = modules
        self.keyMap = {}
        for mapping in LircListener._showMappings:
            for key in mapping['keys']:
                self.keyMap[key] = mapping
        super(LircListener, self).__init__()
    def onKey(self, key, remote):
        if key in self.keyMap:
            config = self.keyMap[key]
            args = []
            if 'args' in config: args = config['args'][:]
            getattr(self.modules[config['module']], config['method'])(*tuple(args))

if __name__ == '__main__':
    Messenger.addOutput(ConsoleOutput())
    Messenger.addOutput(LCDOutput())
    Messenger.addOutput(Messaging())

    universe = Universe()
    output = Output.factory('LPD8806Output', 180)
    output.addFilter(AlphaFilter())
    #output = Output.factory('WebsocketOutput')
    universe.setOutput(output)

    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['lpd8806', 'strip'])
    
    universe = Universe()
    universe.setOutput(Output.factory('SerialOutput', 0, 32))

    for i in range(4):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['dimmer', 'old'])

    # the first of the channels on the secondary board is still unused, that's why counting starts at 13
    for i in range(3):
        fixture = Dimmer()
        fixture.mapToUniverse(universe, 13 + i)
        fixture.addTags(['dimmer', 'ikea', 'old'])

    universe = Universe()
    universe.setOutput(Output.factory('SerialOutput', 1, 150))
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['ws2801', 'pixel', 'wall'])

    '''
    universe = Universe()
    universe.setOutput(Output.factory('SerialOutput', 2, 150))
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixture.addTags(['ws2801', 'pixel', 'tree'])
    '''

    bands = []
    universe = Universe()
    universe.setOutput(Output.factory('DEOutput', '0000000000001337'))
    for i in range(2):
        fixture = StairvillePAR()
        fixture.mapToUniverse(universe, i * 5)
        fixture.addTags(['dmx'])
        for c in ['red', 'green', 'blue']:
            bands.append(fixture.getNamedChannel(c))

    for i in range(4):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, 20 + i * 6)
        fixture.addTags(['dmx', 'par'])

    for i in range(100):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, 99 + i * 3)
        fixture.addTags(['ws2801', 'pixel', 'balcony'])

    for i in range(6):
        fixture = Dimmer()
        fixture.mapToUniverse(universe, 56 + i)
        fixture.addTags(['halogen', '230v'])

    #universe = Universe()
    #universe.setOutput(Output.factory('SocketOutput', 'fft'))
    #universe.setOutput(Output.factory('SerialOutput', 2, 32))
    #for i in range(32):
    #    band = Dimmer()
    #    band.mapToUniverse(universe, i)
    #    bands.append(band)


    subMaster = SubMaster(['strip red', 'strip green', 'strip blue', 'strip white', 'dimmer red', 'dimmer green', 'dimmer blue', 'dimmer white', 'dj', 'PARs red', 'PARs green', 'PARs blue', 'PARs white', 'pixel red', 'pixel green', 'pixel blue', 'pixel white', 'master red', 'master green', 'master blue'], 20)
    for name in ['red', 'green', 'blue']:
        subMaster.mapChannel('master ' + name, subMaster.getChannel('pixel ' + name))
        subMaster.mapChannel('master ' + name, subMaster.getChannel('strip ' + name))
        subMaster.mapChannel('master ' + name, subMaster.getChannel('dimmer ' + name))
        subMaster.mapChannel('master ' + name, subMaster.getChannel('PARs ' + name))

        subMaster.mapChannel('pixel white', subMaster.getChannel('pixel ' + name))
        subMaster.mapChannel('strip white', subMaster.getChannel('strip ' + name))
        subMaster.mapChannel('dimmer white', subMaster.getChannel('dimmer ' + name))
        subMaster.mapChannel('PARs white', subMaster.getChannel('PARs ' + name))

        subMaster.mapChannels('strip ' + name, FixtureManager.filter(lambda f : f.hasTag('strip')).getChannels(name))
        subMaster.mapChannels('pixel ' + name, FixtureManager.filter(lambda f : f.hasTag('pixel')).getChannels(name))
        subMaster.mapChannels('dimmer ' + name, FixtureManager.filter(lambda f : f.hasTag('rgb', 'dimmer')).getChannels(name))
        subMaster.mapChannels('PARs ' + name, FixtureManager.filter(lambda f : f.hasTag('par')).getChannels(name))

    subMaster.mapChannels('dj', FixtureManager.filter(lambda f : f.hasTag('ikea')).getChannels('brightness'))

    subMaster.mapChannels('halogen', FixtureManager.filter(lambda f : f.hasTag('halogen')).getChannels('brightness'))

    bank = Bank("default")
    ChannelMapping(bank.universe[1], subMaster.getChannel('PARs red'))
    ChannelMapping(bank.universe[3], subMaster.getChannel('PARs green'))
    ChannelMapping(bank.universe[5], subMaster.getChannel('PARs blue'))
    ChannelMapping(bank.universe[0], subMaster.getChannel('dimmer red'))
    ChannelMapping(bank.universe[2], subMaster.getChannel('dimmer green'))
    ChannelMapping(bank.universe[4], subMaster.getChannel('dimmer blue'))
    ChannelMapping(bank.universe[7], subMaster.getChannel('dj'))
    ChannelMapping(bank.universe[6], subMaster.getChannel('halogen'))
    ChannelMapping(bank.universe[8], subMaster.getChannel('dimmer red'))
    ChannelMapping(bank.universe[9], subMaster.getChannel('dimmer green'))
    ChannelMapping(bank.universe[10], subMaster.getChannel('dimmer blue'))
    ChannelMapping(bank.universe[11], subMaster.getChannel('dimmer white'))
    ChannelMapping(bank.universe[12], subMaster.getChannel('dj'))
    remoteServer.addBank(bank)

    bank = Bank("master")
    ChannelMapping(bank.universe[1], subMaster.getChannel('master red'))
    ChannelMapping(bank.universe[3], subMaster.getChannel('master green'))
    ChannelMapping(bank.universe[5], subMaster.getChannel('master blue'))
    remoteServer.addBank(bank)
    
    showManager = ShowManager()

    showManager.addShow('knightrider', 'Knight Rider', [
        'KnightRider',
        {'red':255, 'green':0, 'blue':0},
        {'red':0,   'green':0, 'blue':0}
    ])
    showManager.addShow('snow', 'Snow', ['Snow'])
    showManager.addShow('colorfader', 'Color Fader', ['ColorFader'])
    showManager.addShow('colorwheel', 'Color Wheel', ['ColorWheel'])
    showManager.addShow('strobe', 'Strobe', ['Strobe', 60, 64])
    showManager.addShow('vu', 'VU Meter', ['VUMeter', 'hw:1,0'])
    showManager.addShow('fft', 'FFT Show', ['FFT'])
    showManager.addShow('bpmstrobe', 'BPM Strobe', ['BPMStrobe'])
    showManager.addShow('police', 'Police', ['Police'])
    showManager.addShow('directfft', 'FFT Direct', ['DirectFFT', bands])
    showManager.addShow('twinkle', 'Twinkle', ['Twinkle'])
    showManager.addShow('wakelight', 'Wakelight', ['Wakelight'])
    showManager.addShow('lichterkette', 'Lichterkette', ['Lichterkette'])
    showManager.addShow('lichterketteb', 'Lichterkette @ Balkon', ['Lichterkette'], lambda x: x.hasTag('balcony'))
    showManager.addShow('parblip', 'Par Blip', ['PARBlip'])

    lircListener = LircListener({
        "subMaster":subMaster,
        "showManager":showManager
    })

    lirc = LircClient(lircListener)
    #output.addListener(WsListener(lircListener))

    #MidiBridge(subMaster)

    LightWake(showManager)

    run = True
    while run:
        try:
            time.sleep(10)
        except (KeyboardInterrupt):
            showRunner.stopCurrentShow()
            Output.stopAll()
            run = False
