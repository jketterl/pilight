import threading
from control import Controllable
from module import ShowRunner
from fixture import FixtureManager
from message import Messenger

class Show(threading.Thread):
    def __init__(self, filter = None):
        self.endEvent = threading.Event()
        self.doRun = True
        if filter is None:
            self.fixtureList = FixtureManager
        else:
            self.fixtureList = FixtureManager.filter(filter)
        super(Show, self).__init__();
    def stop(self):
        self.doRun = False
    def waitForEnd(self):
        while not self.endEvent.is_set():
            self.endEvent.wait(60)
    def setParams(self, **kwargs):
        # override in child classes if available
        pass

class ShowManager(Controllable):
    def __init__(self, *args, **kwargs):
        super(ShowManager, self).__init__(*args, **kwargs)
        self.shows = {}
        self.runningShows = {}

    def getId(self):
        return 'showmanager'
    def getShows(self, **kwargs):
        res = []
        for id in self.shows:
            show = self.shows[id]
            res.append({'id':id, 'name':show['name'], 'running': id in self.runningShows})
        return res
    def addShow(self, id, name, definition, filter = None):
        self.shows[id] = {'name':name, 'definition':definition, 'filter':filter}
    def startShow(self, id=None, **kwargs):
        if id is None: return
        if id in self.runningShows: return
        if not id in self.shows: return
        showParams = self.shows[id]
        args = showParams['definition'][:]

        Messenger.displayMessage('starting show %s' % str(id))
        runner = ShowRunner()
        runner.startShow(*tuple(args), filter = self.shows[id]['filter'])
        self.runningShows[id] = runner
        self.emit({'show':id, 'running':True})
    def stopShow(self, id, **kwargs):
        if not id in self.runningShows: return
        Messenger.displayMessage('stopping show %s' % str(id))
        self.runningShows[id].stopCurrentShow()
        del self.runningShows[id]
        self.emit({'show':id, 'running':False})
    def stopAllShows(self, **kwargs):
        keys = self.runningShows.keys()
        for id in keys: self.stopShow(id)
    def getShowInstance(self, id):
        if not id in self.runningShows: return None
        return self.runningShows[id].currentShow
    def isRunning(self, id):
        return id in self.runningShows

class ShowFaderMapping(object):
    def __init__(self, channel, showManager, showName, param = None):
        self.showManager = showManager
        self.showName = showName
        self.param = param
        channel.addListener(self)
    def onValueChange(self, source, value):
        if (value > 0):
            self.showManager.startShow(self.showName)
            if self.param is None: return
            i = self.showManager.getShowInstance(self.showName)
            if not i is None: i.setParams(**{self.param: value})
        else:
            self.showManager.stopShow(self.showName)

class ShowButtonMapping(object):
    def __init__(self, channel, showManager, showName):
        self.showManager = showManager
        self.showName = showName
        channel.addListener(self)
    def onValueChange(self, source, value):
        # trigger only on button release
        if value > 0: return
        if self.showManager.isRunning(self.showName):
            self.showManager.stopShow(self.showName)
            self.running = False
        else:
            self.showManager.startShow(self.showName)
            self.running = True
