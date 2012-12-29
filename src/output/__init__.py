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

    def stop(self):
        pass    

    @staticmethod
    def factory(classname, *args, **kwargs):
        mod = __import__("output.%s" % classname, fromlist=[classname])
        cls = getattr(mod, classname)
        out = cls(*args, **kwargs)
        if not hasattr(Output, '_outputs'): Output._outputs = []
        Output._outputs.append(out)
        return out
    @staticmethod
    def stopAll():
        for out in Output._outputs:
            out.stop()
