class Output(object):
    def displayMessage(self, message):
        pass

class ConsoleOutput(Output):
    def displayMessage(self, message):
        print message

from lcdproc.server import Server
from threading import Timer

class LCDOutput(Output):
    def __init__(self):
        self.lcd = Server()
        self.lcd.start_session()
        self.screen = self.lcd.add_screen("Message")
        self.screen.add_title_widget("title", "pilight Message")
        self.screen.set_duration(5)
        self.screen.set_priority("hidden")
        self.textWidget = self.screen.add_string_widget("message", text="", x=1, y=2)
    def displayMessage(self, message):
        self.textWidget.set_text(message)
        self.screen.set_priority("foreground")
        self.scheduleHide()
    def scheduleHide(self):
        def hide():
            self.screen.set_priority("hidden")
            del self.timer

        if hasattr(self, "timer"): self.timer.cancel()
        self.timer = Timer(5, hide)
        self.timer.start()
