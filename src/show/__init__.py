import threading
from control import Controllable
from module import ShowRunner

class Show(threading.Thread):
    def __init__(self):
        self.endEvent = threading.Event()
        self.doRun = True
        super(Show, self).__init__();
    def stop(self):
        self.doRun = False
    def waitForEnd(self):
        while not self.endEvent.is_set():
            self.endEvent.wait(60)

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
    def addShow(self, id, name, definition):
        self.shows[id] = {'name':name, 'definition':definition}
    def startShow(self, id=None, **kwargs):
        if id is None: return
        if id in self.runningShows: return
        args = self.shows[id]['definition'][:]

        runner = ShowRunner()
        runner.startShow(*tuple(args))
        self.runningShows[id] = runner
        self.emit({'show':id, 'running':True})
    def stopShow(self, id = None, **kwargs):
        def stopShow(id):
            self.runningShows[id].stopCurrentShow()
            del self.runningShows[id]
            self.emit({'show':id, 'running':False})
        if id is None:
            # stop all shows
            pass
        else:
            stopShow(id)
    def setShow(self, show):
        self.show = show
        self.emit({'show':show})
