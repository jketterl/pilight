import sys
sys.path.append('../vendors/python-artnet/src/')

from output import Output
from filter import ScalingAlphaFilter
from input import SocketInput
from universe import Universe

if __name__ == '__main__':

    output = Output.factory('WS2801Output', channels=150)
    output.addFilter(ScalingAlphaFilter(255))

    universe = Universe(150)
    universe.setOutput(output)

    input = SocketInput(universe, '192.168.4.2', 'ws2801')
