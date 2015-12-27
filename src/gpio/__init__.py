import RPi.GPIO as GPIO
import time

from universe import Universe

class GPIOInput(object):
    def __init__(self, gpios, invert = True):
        GPIO.setmode(GPIO.BCM)
        self.gpios = gpios
        self.universe = Universe(len(gpios))
        self.invert = invert
        GPIO.setup(gpios, GPIO.IN)

        super(GPIOInput, self).__init__()

        def gpioChange(index):
            def f(channel):
                self.universe[index].setValue(255 if GPIO.input(channel) != self.invert else 0)
            return f

        for index, gpio in enumerate(self.gpios):
            GPIO.add_event_detect(gpio, GPIO.BOTH, callback = gpioChange(index))
