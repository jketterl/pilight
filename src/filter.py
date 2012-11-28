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
