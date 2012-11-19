'''
Created on 01.11.2012

@author: jakob
'''
from universe import Universe
from fixture import RGBFixture
from output import LPD8806Output
from threading import Thread
import random, time

class Snowflake(Thread):
    def __init__(self, device):
        self.device = device
        super(Snowflake, self).__init__()
    def run(self):
        for i in range(255, 0, -8):
            self.device.setChannels({'red':i,'green':i,'blue':i})
            time.sleep(.05)
        self.device.setChannels({'red':0,'green':0,'blue':0})

if __name__ == '__main__':
    universe = Universe()
    universe.setOutput(LPD8806Output(180))

    fixtures = []
    for i in range(60):
        fixture = RGBFixture()
        fixture.mapToChannels({
            'red' : universe[i * 3 + 1],
            'green' : universe[i * 3],
            'blue' : universe[i * 3 + 2]
        })
        fixtures.append(fixture)
    
    while True:
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

        for n in range(15):
            for i in range(len(fixtures)):
                fixtures[i - 1].setChannels({'red':0,'green':0,'blue':0})
                fixtures[i].setChannels({'red':255,'blue':255,'green':255})
                time.sleep(.01)

            for i in range(len(fixtures) - 2, 0, -1):
                fixtures[i + 1].setChannels({'red':0,'green':0,'blue':0})
                fixtures[i].setChannels({'red':255,'blue':255,'green':255})
                time.sleep(.01)

        for i in range(200):
            channel = random.randint(0, len(fixtures) - 1)
            flake = Snowflake(fixtures[channel])
            flake.start()
            time.sleep(.2)
        time.sleep(10)
