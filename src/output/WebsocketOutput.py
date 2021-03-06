'''
Created on Nov 19, 2012

@author: jketterl
'''

from .ThreadedOutput import ThreadedOutput
from tornado import ioloop, web, websocket
import threading, json

class MyWebsocket(websocket.WebSocketHandler):
    def open(self):
        WebsocketOutput.connections.append(self)
    def on_message(self, message):
        WebsocketOutput._receive(message)
    def on_close(self):
        WebsocketOutput.connections.remove(self)
        
class WebsocketListener(object):
    def receive(self, message):
        pass

class WebsocketOutput(ThreadedOutput):
    app = None
    connections = []
    @staticmethod
    def getApp():
        if WebsocketOutput.app is None:
            WebsocketOutput.app = web.Application([(r"/socket", MyWebsocket)])
            WebsocketOutput.app.listen(8080)
            threading.Thread(target = ioloop.IOLoop.instance().start).start()
            WebsocketOutput.instances = []
            
        return WebsocketOutput.app
    
    def __init__(self):
        WebsocketOutput.getApp()
        WebsocketOutput.instances.append(self)
        self.listeners = []
        super(WebsocketOutput, self).__init__()
        
    def applyChanges(self, changes):
        self.send(changes)
    
    def send(self, changes):
        for conn in WebsocketOutput.connections:
            conn.write_message(json.dumps(changes));
            
    def addListener(self, listener):
        self.listeners.append(listener)
    
    @staticmethod        
    def _receive(message):
        for out in WebsocketOutput.instances:
            out.receive(message)
            
    def receive(self, message):
        for listener in self.listeners:
            listener.receive(message);