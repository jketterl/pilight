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
    universe.setOutput(LPD8806Output(180))

    fixtures = []
    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToChannels({
            'red' : universe[i * 3 + 2],
            'green' : universe[i * 3 +1],
            'blue' : universe[i * 3]
        })
	fixtures.append(fixture)
    
    while True:
	for fixture in fixtures:
            fixture.setChannels({'red':random.randint(0, 255),
                                 'green':random.randint(0, 255),
                                 'blue':random.randint(0, 255)})
        time.sleep(1)
