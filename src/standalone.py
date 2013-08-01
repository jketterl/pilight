from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import RGBFixture
from module import ShowRunner, SubMaster

ControlServer.getInstance()

if __name__ == '__main__':
    fixtures = []

    subMaster = SubMaster(['red', 'green', 'blue'], 3)

    universe = Universe()
    universe.setOutput(Output.factory('WS2801Output', channels=150))
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))

    showRunner = ShowRunner()
    showRunner.startShow('KnightRider', fixtures, {'red':255}, {'red':0})
