from . import Output
import usbdmx

class DEOutput(Output):
    def __init__(self, serial):
        super(DEOutput, self).__init__()
        self.device = filter(lambda d : d.serial == serial, usbdmx.scan())[0]
        self.device.open()
        self.device.mode(6)
    def _setChannelValue(self, channel, value):
        self.device.set_dmx(channel, value)
