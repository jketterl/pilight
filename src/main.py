'''
Created on 01.11.2012

@author: jakob
'''

import sys
sys.path.append('../vendors/python-artnet/src/')
sys.path.append('../vendors/adafruit/Adafruit_PWM_Servo_Driver/')

from universe import Universe
from filter import AlphaFilter
from fixture import RGBFixture, Dimmer
from output import Output
import time
from lirc import *
from module import SubMaster, ShowRunner
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
        super(LightWake, self).__init__(datetime.time(05, 45))
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
            'method':'stopShow'
        },
        {
            'keys':['red','R'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['red']
        },                     
        {
            'keys':['green','G'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['green']
        },                     
        {
            'keys':['blue','B'],
            'module':'subMaster',
            'method':'selectChannel',
            'args':['blue']
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

    subMaster = SubMaster(['red', 'green', 'blue', 'dj', 'tree red', 'tree green', 'tree blue', 'tree white'], 8)
    for name in ['red', 'green', 'blue']:
        subMaster.mapChannel(name, subMaster.getChannel('tree ' + name))
        subMaster.mapChannel('tree white', subMaster.getChannel('tree ' + name))

    fixtures = []
    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))
    
    universe = Universe()
    universe.setOutput(Output.factory('SerialOutput', 0, 32))

    for i in range(4):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))

    # the fist of the channels on the secondary board is still unused, that's why counting starts at 13
    for i in range(3):
        fixture = Dimmer()
        fixture.mapToUniverse(universe, 13 + i)
        subMaster.mapChannel('dj', fixture.getNamedChannel('brightness'))

    universe = Universe()
    #universe.setOutput(Output.factory('SocketOutput', 'ws2801'))
    universe.setOutput(Output.factory('SerialOutput', 1, 150))
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            #subMaster.mapChannel(name, fixture.getNamedChannel(name))
            subMaster.mapChannel('tree ' + name, fixture.getNamedChannel(name))

    bands = []
    universe = Universe()
    universe.setOutput(Output.factory('SocketOutput', 'fft'))
    #universe.setOutput(Output.factory('SerialOutput', 2, 32))
    for i in range(32):
        band = Dimmer()
        band.mapToUniverse(universe, i)
        bands.append(band)


    showRunner = ShowRunner()
    
    showManager = ShowManager(fixtures, runner = showRunner)

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
    showManager.addShow('directffct', 'FFT Direct', ['DirectFFT', bands])
    showManager.addShow('twinkle', 'Twinkle', ['Twinkle'])
    showManager.addShow('wakelight', 'Wakelight', ['Wakelight'])
    showManager.addShow('lichterkette', 'Lichterkette', ['Lichterkette'])

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
