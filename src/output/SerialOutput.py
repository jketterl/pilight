from .ThreadedOutput import ThreadedOutput
import serial, struct

class Writer(object):
    _writer = None
    @staticmethod
    def getWriter():
        if Writer._writer is None:
            Writer._writer = Writer()
        return Writer._writer
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200)
    def write(self, data):
        self.ser.write(data)
        self.ser.flushInput()

class SerialOutput(ThreadedOutput):
    def __init__(self, deviceId, *args, **kwargs):
        super(SerialOutput, self).__init__(*args, **kwargs)
        self.deviceId = deviceId

    def applyChanges(self, changes):
        message = ''
        for key in changes:
            message += struct.pack('BB', key, changes[key])
        message = 'SYNC' + struct.pack('<BH', self.deviceId, len(message)) + message
        Writer.getWriter().write(message)
