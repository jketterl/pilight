from . import Output
from Adafruit_PWM_Servo_Driver import PWM

class AdafruitPWMOutput(Output):
    def __init__(self, address = 0x40, bus = 0):
        self.pwm = PWM(address, False, bus)
        self.pwm.setPWMFreq(1600)
        super(AdafruitPWMOutput, self).__init__()
    def _setChannelValue(self, channel, value):
        self.pwm.setPWM(channel, 0, value)
