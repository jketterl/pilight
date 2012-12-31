class Filter(object):
    def filter(self, input):
        return input

class AlphaFilter(Filter):
    def __init__(self):
        self.filterTable = [0] * 256
        for i in range(256):
            self.filterTable[i] = int(round(255.0 * (i / 255.0) ** 2.2))
    def filter(self, input):
        return self.filterTable[input]

class ScalingFilter(Filter):
    def __init__(self, maxOut):
        self.max = maxOut
    def filter(self, input):
        return input * self.max / 256

class ScalingAlphaFilter(AlphaFilter):
    def __init__(self, maxOut):
        self.filterTable = [0] * 256
        for i in range(256):
            self.filterTable[i] = int(round(maxOut * (i / 255.0) ** 2.2))
