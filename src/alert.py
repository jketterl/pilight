import threading, datetime

class Alert(object):
    def __init__(self, time):
        self.time = time
        self.schedule()
    def schedule(self):
        def r():
            self.run()
            self.schedule()

        # first, take today and apply the specified time
        next = datetime.datetime.combine(datetime.date.today(), self.time)

        # if the alert time is already passed today, goto tomorrow
        if (next < datetime.datetime.now()): next += datetime.timedelta(days=1)

        # only on weekdays, please!
        while next.weekday() >= 5: next += datetime.timedelta(days=1)

        # calculate the time to the next alert
        delta = next - datetime.datetime.now()
        interval = delta.total_seconds()
        print "setting alert in %d seconds" % interval

        # and set a timer
        threading.Timer(interval, r).start()
    def run(self):
        pass
