'''
Created on 19.12.2012

@author: jakob
'''

from universe import Universe
from channel import Channel, ChannelMapping

from lcdproc.screen import Screen
from threading import Timer

class LCDMessageScreen(Screen):
    pass

class SubMaster(Universe):
    def __init__(self, channelNames = [], count = 512, lcd = None):
        super(SubMaster, self).__init__(count)
        master = Channel()
        self.channelMap = {}
        for index, name in enumerate(channelNames):
            channel = self[index]
            self.channelMap[name] = channel 
            ChannelMapping(master, channel)
        self.channelMap['master'] = master
        self.lcd = lcd
    def selectChannel(self, channel, fixtures):
        self.currentChannel = self.getChannel(channel)
        self.showMessage('selected: %s' % channel)
    def getChannel(self, name):
        return self.channelMap[name]
    def increaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() + 10)
    def decreaseValue(self, *args):
        self.currentChannel.setValue(self.currentChannel.getValue() - 10)
    def mapChannel(self, name, target):
        ChannelMapping(self.getChannel(name), target)
    def showMessage(self, message):
        widget = self.getMessageWidget()
        screen = self.getMessageScreen()
        if widget is None or screen is None: return
        widget.set_text(message)
        screen.set_priority('foreground')
        def lowerPriority():
            screen.set_priority('hidden')
        Timer(5, lowerPriority).start()
    def getMessageScreen(self):
        if self.lcd is None: return None
        if not hasattr(self, '_messageScreen'):
            self._messageScreen = self.lcd.add_screen("Message")
            self._messageScreen.add_title_widget("title", "pilight message")
            self._messageScreen.set_duration(5)
            self._messageScreen.set_priority("hidden")
        return self._messageScreen
    def getMessageWidget(self):
        screen = self.getMessageScreen()
        if screen is None: return None
        if not hasattr(self, '_messageWidget'):
            self._messageWidget = screen.add_string_widget('message', text="", x=1, y=2)
        return self._messageWidget
