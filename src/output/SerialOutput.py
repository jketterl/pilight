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

    def xorChecksum(self, input):
        result = 0
        for byte in input:
            result ^= ord(byte)
        return result

    def applyChanges(self, changes):
        super(SerialOutput, self).applyChanges(changes)
        if changes and len(changes) <= self.channelCount / 2:
            # delta frame
            message = ''
            for key in changes:
                message += struct.pack('BB', key, changes[key])
            if (len(message) > 512): print "delta frame with %i bytes" % len(message)
            header = struct.pack('<BBH', self.deviceId, 0x01, len(message))
            message = 'SYNC' + header + struct.pack('<BB', self.xorChecksum(header), self.xorChecksum(message)) + message
        else:
            # alpha frame
            message = ''
            for value in self.buffer:
                message += struct.pack('B', value)
            if (len(message) > 512): print "alpha frame with %i bytes" % len(message)
            header = struct.pack('<BBH', self.deviceId, 0x00, len(message))
            message = 'SYNC' + header + struct.pack('<BB', self.xorChecksum(header), self.xorChecksum(message)) + message
        Writer.getWriter().write(message)
