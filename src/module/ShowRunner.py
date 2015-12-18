'''
Created on 19.12.2012

@author: jakob
'''

class ShowRunner(object):
    def __init__(self):
        self.currentShow = None
        super(ShowRunner, self).__init__()
    def startShow(self, showClass, *args, **kwargs):
        self.stopCurrentShow()

        mod = __import__("show.%s" % showClass, fromlist=[showClass])
        cls = getattr(mod, showClass)
        self.currentShow = cls(*args, **kwargs)
        self.currentShow.start()
    def stopCurrentShow(self, *args):
        if self.currentShow is None: return
        self.currentShow.stop()
        self.currentShow.waitForEnd()
        self.currentShow = None
