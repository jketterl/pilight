'''
Created on 01.11.2012

@author: jakob
'''

class Output(object):
    def setChannel(self, channel, value):
        pass
    
    @staticmethod
    def factory(classname, *args, **kwargs):
        mod = __import__("output.%s" % classname, fromlist=[classname])
        cls = getattr(mod, classname)
        return cls(*args, **kwargs)
