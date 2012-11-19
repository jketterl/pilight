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
        pass
    def on_close(self):
        WebsocketOutput.connections.remove(self)

class WebsocketOutput(ThreadedOutput):
    app = None
    connections = []
    @staticmethod
    def getApp():
        if WebsocketOutput.app is None:
            WebsocketOutput.app = web.Application([(r"/socket", MyWebsocket)])
            WebsocketOutput.app.listen(8080)
            threading.Thread(target = ioloop.IOLoop.instance().start).start()
            
        return WebsocketOutput.app
    
    def __init__(self):
        WebsocketOutput.getApp()
        super(WebsocketOutput, self).__init__()
        
    def applyChanges(self, changes):
        self.send(changes)
    
    def send(self, changes):
        for conn in WebsocketOutput.connections:
            conn.write_message(json.dumps(changes));