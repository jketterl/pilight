class Messenger(object):
    outputs = []
    @staticmethod
    def displayMessage(message):
        for output in Messenger.outputs:
            output.displayMessage(message)
    @staticmethod
    def addOutput(output):
        Messenger.outputs.append(output)
