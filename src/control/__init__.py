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
        if not 'module' in message: return
        if not 'command' in message: return
        controllable = ControlServer.getInstance().getControllable(message['module'])
        params = {}
        if 'params' in message: params = message['params']
        response = {'status':'OK','data':controllable.executeCommand(message['command'], **params)}
        if 'sequence' in message: response['sequence'] = message['sequence']
        self.write_message(json.dumps(response))
    def on_close(self):
        pass
        
class ControlServer(object):
    _instance = None
    @staticmethod
    def getInstance():
        if ControlServer._instance is None:
            ControlServer._instance = ControlServer()
        return ControlServer._instance
    def __init__(self):
        self.app = web.Application([(r"/control", ControlSocket)])
        self.app.listen(9001)
        threading.Thread(target = ioloop.IOLoop.instance().start).start()

        self.controllables = {}
    def registerControllable(self, controllable):
        self.controllables[controllable.getId()] = controllable
    def getControllable(self, id):
        return self.controllables[id]

class Controllable(object):
    def __init__(self, *args, **kwargs):
        super(Controllable, self).__init__(*args, **kwargs)
        ControlServer.getInstance().registerControllable(self)
    def executeCommand(self, command, **kwargs):
        return getattr(self, command)(**kwargs)

