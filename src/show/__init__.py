import threading
from control import Controllable
from module import ShowRunner

class Show(threading.Thread):
    def __init__(self, fixtures):
        self.endEvent = threading.Event()
        self.doRun = True
        self.fixtures = fixtures
        super(Show, self).__init__();
    def stop(self):
        self.doRun = False
    def waitForEnd(self):
        while not self.endEvent.is_set():
            self.endEvent.wait(60)

class ShowManager(Controllable):
    def __init__(self, fixtures, runner = None, *args, **kwargs):
        super(ShowManager, self).__init__(*args, **kwargs)
        if runner is None:
            self.runner = ShowRunner()
        else:
            self.runner = runner
        self.shows = {}
        self.fixtures = fixtures
    def getId(self):
        return 'showmanager'
    def getShows(self, **kwargs):
        res = []
        for id in self.shows:
            res.append({'id':id, 'name':self.shows[id]['name']})
        return res
    def addShow(self, id, name, definition):
        self.shows[id] = {'name':name, 'definition':definition}
    def startShow(self, id=None, **kwargs):
        if id is None: return
        args = self.shows[id]['definition'][:]
        # always pass a list of fixtures as the second parameter
        args.insert(1, self.fixtures)

        self.runner.startShow(*tuple(args))
    def stopShow(self, **kwargs):
        self.runner.stopCurrentShow()
        
