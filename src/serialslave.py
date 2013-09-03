from output import Output
from input import SocketInput
from universe import Universe

if __name__ == '__main__':

    output = Output.factory('SerialOutput', 1)

    universe = Universe(150)
    universe.setOutput(output)

    input = SocketInput(universe, '192.168.4.2', 'ws2801')
