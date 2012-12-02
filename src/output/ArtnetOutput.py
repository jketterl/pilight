from .BufferedOutput import BufferedOutput

class ArtnetOutput(BufferedOutput):
    def __init__(self, target):
        self.target = target
        super(ArtnetOutput, self).__init__(256)
    def write(self):
        print self.buffer
