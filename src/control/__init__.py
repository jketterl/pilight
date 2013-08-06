'''
Created on Nov 19, 2012

@author: jketterl
'''

from tornado import ioloop, web, websocket
import threading, json

class ControlSocket(websocket.WebSocketHandler):
    def open(self):
        print "socket opened!"
    def on_message(self, message):
        message = json.loads(message)
        if not 'module' in message:
            controllable = ControlServer.getInstance()
        else:
            controllable = ControlServer.getInstance().getControllable(message['module'])

        if controllable is None: return
        if not 'command' in message: return
        params = {}
        if 'params' in message: params = message['params']

        try:
            response = {'status':'OK','data':controllable.executeCommand(message['command'], **params)}
        except Exception as e:
            print e
            response = {'status':'EXCEPTION'}

        if 'sequence' in message: response['sequence'] = message['sequence']
        self.write_message(json.dumps(response))
    def on_close(self):
        pass
        
class Controllable(object):
    def __init__(self, *args, **kwargs):
        super(Controllable, self).__init__(*args, **kwargs)
        ControlServer.getInstance().registerControllable(self)
    def executeCommand(self, command, **kwargs):
        return getattr(self, command)(**kwargs)

class ControlServer(Controllable):
    _instance = None
    @staticmethod
    def getInstance():
        if ControlServer._instance is None:
            ControlServer._instance = ControlServer()
        return ControlServer._instance
    def __init__(self, *args, **kwargs):
        self.app = web.Application([(r"/control", ControlSocket)])
        self.app.listen(9001)
        threading.Thread(target = ioloop.IOLoop.instance().start).start()

        self.controllables = {}
        # instead of the super constructor call
        self.registerControllable(self)
    def registerControllable(self, controllable):
        self.controllables[controllable.getId()] = controllable
    def getControllable(self, id):
        try:
            return self.controllables[id]
        except KeyError:
            return None
    def getControllables(self):
        result = []
        for key in self.controllables:
            controllable = self.controllables[key]
            result.append({'id':controllable.getId(), 'type':controllable.__class__.__name__});
        return result
    def getId(self):
        return 'controlserver'
