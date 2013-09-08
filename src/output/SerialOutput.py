from .BufferedOutput import BufferedOutput
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

class SerialOutput(BufferedOutput):
    def __init__(self, deviceId, *args, **kwargs):
        super(SerialOutput, self).__init__(*args, **kwargs)
        self.deviceId = deviceId

    def applyChanges(self, changes):
        if changes:
            message = ''
            for key in changes:
                message += struct.pack('BB', key, changes[key])
            message = 'SYNC' + struct.pack('<BBH', self.deviceId, 0x01, len(message)) + message
        else:
            message = ''
            for value in self.buffer:
                message += struct.pack('B', value)
            message = 'SYNC' + struct.pack('<BBH', self.deviceId, 0x00, len(message)) + message
        Writer.getWriter().write(message)
        super(SerialOutput, self).applyChanges(changes)
