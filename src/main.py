'''
Created on 01.11.2012

@author: jakob
'''
from universe import Universe
from fixture import RGBFixture
from output import ConsoleOutput

if __name__ == '__main__':
    universe = Universe()
    universe.setOutput(ConsoleOutput())
    fixture = RGBFixture()
    fixture.mapToChannels({
        'red' : universe[2],
        'green' : universe[1],
        'blue' : universe[0]
    })
    
    fixture.setChannels({'red':10,'green':20,'blue':30});