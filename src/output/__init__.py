'''
Created on 01.11.2012

@author: jakob
'''

class Output(object):
    def __init__(self):
        self.filters = []
        super(Output, self).__init__()

    def setChannel(self, channel, value):
        for filter in self.filters:
            value = filter.filter(value)
        self._setChannelValue(channel, value)

    def _setChannelValue(self, channel, value):
        pass

    def addFilter(self, filter):
        self.filters.append(filter)
    
    @staticmethod
    def factory(classname, *args, **kwargs):
        mod = __import__("output.%s" % classname, fromlist=[classname])
        cls = getattr(mod, classname)
        return cls(*args, **kwargs)
