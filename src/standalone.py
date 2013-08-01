from control import ControlServer, Controllable
from universe import Universe
from output import Output
from fixture import RGBFixture
from module import ShowRunner, SubMaster
from filter import AlphaFilter

ControlServer.getInstance()

if __name__ == '__main__':
    fixtures = []

    subMaster = SubMaster(['red', 'green', 'blue'], 3)

    universe = Universe()
    output = Output.factory('WS2801Output', channels=150)
    output.addFilter(AlphaFilter())
    universe.setOutput(output)
    for i in range(50):
        fixture = RGBFixture(channelSequence='RGB')
        fixture.mapToUniverse(universe, i * 3)
        fixtures.append(fixture)
        for name in ['red', 'green', 'blue']:
            subMaster.mapChannel(name, fixture.getNamedChannel(name))

    showRunner = ShowRunner()
