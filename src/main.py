'''
Created on 01.11.2012

@author: jakob
'''
from universe import Universe
from fixture import RGBFixture
from output import LPD8806Output
import random, time

if __name__ == '__main__':
    universe = Universe()
    universe.setOutput(LPD8806Output(480))
    fixture = RGBFixture()
    fixture.mapToChannels({
        'red' : universe[2],
        'green' : universe[1],
        'blue' : universe[0]
    })
    
    fixture.setChannels({'red':10,'green':20,'blue':30});
    
    while True:
        time.sleep(5)
        fixture.setChannels({'red':random.randint(0, 255),
                             'green':random.randint(0, 255),
                             'blue':random.randint(0, 255)})
        print "channel values set."