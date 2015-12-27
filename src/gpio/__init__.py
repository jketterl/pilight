import RPi.GPIO as GPIO
import time
from threading import Thread

from universe import Universe

class GPIOInput(Thread):
    def __init__(self, gpios, invert = True):
        GPIO.setmode(GPIO.BCM)
        self.gpios = gpios
        self.universe = Universe(len(gpios))
        self.invert = invert
        for gpio in gpios:
            GPIO.setup(gpio, GPIO.IN)

        super(GPIOInput, self).__init__()

        self.start()
    def run(self):
        while (True):
            for index, gpio in enumerate(self.gpios):
                self.universe[index].setValue(255 if GPIO.input(gpio) != self.invert else 0)
            time.sleep(.1)
