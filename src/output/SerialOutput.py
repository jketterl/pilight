from .ThreadedOutput import ThreadedOutput
import serial, struct

class SerialOutput(ThreadedOutput):
    def __init__(self, deviceId, *args, **kwargs):
        super(SerialOutput, self).__init__(*args, **kwargs)
        self.ser = serial.Serial('/dev/ttyAMA0', 115200)
        self.deviceId = deviceId

    def applyChanges(self, changes):
        message = ''
        for key in changes:
            message += struct.pack('BB', key, changes[key])
        message = 'SYNC' + struct.pack('<BH', self.deviceId, len(message)) + message
        self.ser.write(message)
        self.ser.flushInput()
