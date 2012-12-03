'''
Created on 01.11.2012

@author: jakob
'''

import sys
sys.path.append('../vendors/python-artnet/src/')

from universe import Universe
from filter import AlphaFilter
from fixture import RGBFixture
from output import Output
from threading import Thread
import random, time
from lirc import *

class ShowRunner(object):
    def __init__(self):
        self.currentShow = None
        super(ShowRunner, self).__init__()
    def startShow(self, showClass, *args, **kwargs):
        self.stopCurrentShow()
        print 'starting show %s' % showClass

        mod = __import__("show.%s" % showClass, fromlist=[showClass])
        cls = getattr(mod, showClass)
        self.currentShow = cls(*args, **kwargs)
        self.currentShow.start()
    def stopCurrentShow(self):
        if self.currentShow is None: return
        print 'stopping current show'
        self.currentShow.stop()
        self.currentShow.waitForEnd()
        self.currentShow = None

class LircListener(LircDelegate):
    _showMappings = [
        {
            'keys':['1'],
            'show':'VUMeter',
            'args':[
                'hw:1,0'
            ]
        },
        {
            'keys':['2'],
            'show':'KnightRider',
            'args':[
                {'red':255, 'green':0, 'blue':0},
                {'red':0,   'green':0, 'blue':0}
            ]
        },
        {
            'keys':['3'],
            'show':'BPM'
        },
        {
            'keys':['4'],
            'show':'Snow'
        },
        {
            'keys':['5'],
            'show':'ColorFader'
        }
    ]
    def __init__(self, showRunner):
        self.showRunner = showRunner;
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
            
            # always pass a list of fixtures as the first parameter
            args.insert(0, fixtures)
            self.showRunner.startShow(config['show'], *tuple(args))
        elif key == 'stop' or key == 'standby':
            self.showRunner.stopCurrentShow()
            for fixture in fixtures:
                fixture.setChannels({'red':0,'green':0,'blue':0})

if __name__ == '__main__':
    universe = Universe()
    output = Output.factory('LPD8806Output', 180)
    output.addFilter(AlphaFilter())
    universe.setOutput(output)

    fixtures = []
    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToChannels({
            'red' : universe[i * 3 + 1],
            'green' : universe[i * 3],
            'blue' : universe[i * 3 + 2]
        })
        fixtures.append(fixture)
    
    universe = Universe()
    universe.setOutput(Output.factory('ArtnetOutput', 'pilight01'));

    for i in range(4):
        fixture = RGBFixture()
        fixture.mapToChannels({
            'red' : universe[i * 3 + 1],
            'green' : universe[i * 3],
            'blue' : universe[i * 3 + 2]
        })
        fixtures.append(fixture)

    showRunner = ShowRunner()
    lirc = LircClient(LircListener(showRunner))

    run = True
    while run:
        try:
            time.sleep(10)
        except (KeyboardInterrupt):
            showRunner.stopCurrentShow()
            run = False

        '''
        show = BPM(fixtures)
        show.start()
        time.sleep(60)
        show.stop()
        show.waitForEnd()
        
        show = VUMeter(fixtures, 'hw:1,0')
        show.start()
        time.sleep(60)
        show.stop()
        show.waitForEnd()
        
        for i in range(10):
            for fixture in fixtures:
                fixture.setChannels({'red':random.randint(0, 255),
                                     'green':random.randint(0, 255),
                                     'blue':random.randint(0, 255)})
                time.sleep(.01)
            #time.sleep(1)
            for fixture in fixtures:
                fixture.setChannels({'red':0,'green':0,'blue':0})
                time.sleep(.01)
            time.sleep(1)

        show = KnightRider(fixtures, {'red':255,'green':0,'blue':0}, {'red':0,'green':0,'blue':0})
        show.start()
        time.sleep(15)
        show.stop()
        show.waitForEnd()
        '''
