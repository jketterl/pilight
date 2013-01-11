'''
Created on 01.11.2012

@author: jakob
'''

import sys
sys.path.append('../vendors/python-artnet/src/')
sys.path.append('../vendors/adafruit/Adafruit_PWM_Servo_Driver/')

from universe import Universe
from filter import AlphaFilter
from fixture import RGBFixture
from output import Output
import time
from lirc import *
#from output.WebsocketOutput import WebsocketListener
from module import SubMaster, ShowRunner

from message import Messenger
from message.output import ConsoleOutput, LCDOutput

'''
class WsListener(WebsocketListener):
    def __init__(self, lirc):
        self.lirc = lirc
    def receive(self, message):
        self.lirc.onKey(message, None)
'''

class LircListener(LircDelegate):
    _showMappings = [
        {
            'keys':['1'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'VUMeter',
                'hw:1,0'
            ]
        },
        {
            'keys':['2'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'KnightRider',
                {'red':255, 'green':0, 'blue':0},
                {'red':0,   'green':0, 'blue':0}
            ]
        },
        {
            'keys':['3'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'BPM'
            ]
        },
        {
            'keys':['4'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'Snow'
            ]
        },
        {
            'keys':['5'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'ColorFader'
            ]
        },
        {
            'keys':['6'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'ColorWheel'
            ]
        },
        {
            'keys':['7'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'FFT'
            ]
        },
        {
            'keys':['8'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'BPMStrobe'
            ]
        },
        {
            'keys':['9'],
            'module':'showRunner',
            'method':'startShow',
            'args':[
                'Strobe'
            ]
        },
        {
            'keys':['stop','standby'],
            'module':'showRunner',
            'method':'stopCurrentShow'
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
            
            # always pass a list of fixtures as the second parameter
            args.insert(1, fixtures)
            getattr(self.modules[config['module']], config['method'])(*tuple(args))

if __name__ == '__main__':
    Messenger.addOutput(ConsoleOutput())
    Messenger.addOutput(LCDOutput())

    universe = Universe()
    output = Output.factory('LPD8806Output', 180)
    output.addFilter(AlphaFilter())
    #output = Output.factory('WebsocketOutput')
    universe.setOutput(output)

    subMaster = SubMaster(['red', 'green', 'blue', 'dj'], 4)

    fixtures = []
    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name));
    
    universe = Universe()
    universe.setOutput(Output.factory('ArtnetOutput', 'pilight01'));

    for i in range(4):
        fixture = RGBFixture()
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name));

    fixture = RGBFixture()
    fixture.mapToUniverse(universe, 12)
    for name in ['red', 'green', 'blue']:
        subMaster.mapChannel('dj', fixture.getNamedChannel(name))

    showRunner = ShowRunner()
    
    lircListener = LircListener({
        "showRunner":showRunner,
        "subMaster":subMaster
    })

    lirc = LircClient(lircListener)
    #output.addListener(WsListener(lircListener))

    run = True
    while run:
        try:
            time.sleep(10)
        except (KeyboardInterrupt):
            showRunner.stopCurrentShow()
            Output.stopAll()
            run = False
