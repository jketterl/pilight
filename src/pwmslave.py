import sys
sys.path.append('../vendors/python-artnet/src/')
sys.path.append('../vendors/adafruit/Adafruit_PWM_Servo_Driver/')

from output import Output
from filter import ScalingAlphaFilter
from input import ArtnetInput
from universe import Universe

if __name__ == '__main__':

    output = Output.factory('AdafruitPWMOutput', address=0x40, bus=1)
    output.addFilter(ScalingAlphaFilter(4095))

    universe = Universe(16)
    universe.setOutput(output)

    input = ArtnetInput(universe)
