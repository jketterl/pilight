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
        print 'starting show %s' % showClass

        mod = __import__("show.%s" % showClass, fromlist=[showClass])
        cls = getattr(mod, showClass)
        self.currentShow = cls(*args, **kwargs)
        self.currentShow.start()
    def stopCurrentShow(self):
        if self.currentShow is None: return
        print 'stopping current show'
        self.currentShow.stop()
        self.currentShow.waitForEnd()
        self.currentShow = None
