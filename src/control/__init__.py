'''
Created on Nov 19, 2012

@author: jketterl
'''

from tornado import ioloop, web, websocket
import threading, json

class ControlSocket(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(ControlSocket, self).__init__(*args, **kwargs)
        self.listeners = []
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
        params['socket'] = self

        try:
            response = {'status':'OK','data':controllable.executeCommand(message['command'], **params)}
        except Exception as e:
            print e
            response = {'status':'EXCEPTION'}

        if 'sequence' in message: response['sequence'] = message['sequence']
        self.write_message(json.dumps(response))
    def on_close(self):
        print "socket closed"
        for l in self.listeners:
            l.onClose(self)
    def addListener(self, listener):
        self.listeners.append(listener);
        
class Controllable(object):
    def __init__(self, *args, **kwargs):
        super(Controllable, self).__init__(*args, **kwargs)
        ControlServer.getInstance().registerControllable(self)
        self.listeners = []
    def executeCommand(self, command, **kwargs):
        return getattr(self, command)(**kwargs)
    def emit(self, data):
        for l in self.listeners:
            l.write_message(json.dumps({'source':self.getId(), 'data':data}));
    def listen(self, socket = None):
        socket.addListener(self)
        self.listeners.append(socket)
    def onClose(self, socket):
        self.listeners.remove(socket)
    def unregister(self):
        ControlServer.getInstance().unregisterControllable(self)

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
        self.listeners = []
        self.registerControllable(self)
    def registerControllable(self, controllable):
        id = controllable.getId()
        self.controllables[id] = controllable
        self.emit({'add':{'id':id, 'type':controllable.__class__.__name__}})
    def unregisterControllable(self, controllable):
        id = controllable.getId()
        self.emit({'remove':{'id':id}})
        del self.controllables[id]
    def getControllable(self, id):
        try:
            return self.controllables[id]
        except KeyError:
            return None
    def getControllables(self, **kwargs):
        result = []
        for key in self.controllables:
            controllable = self.controllables[key]
            result.append({'id':controllable.getId(), 'type':controllable.__class__.__name__});
        return result
    def getId(self):
        return 'controlserver'
