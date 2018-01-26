from microbus import BusLoop
import threading


class BackgroundBusLoop(BusLoop, threading.Thread):
    def __init__(self):
        super(BackgroundBusLoop, self).__init__()
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

    def schedule(self, route):
        self.lock.acquire()
        super(BackgroundBusLoop, self).schedule(route)
        self.lock.release()

    def remove_scheduled_assignment(self, assignment):
        self.lock.acquire()
        super(BackgroundBusLoop, self).remove_scheduled_assignment(assignment)
        self.lock.release()

    def run(self):
        super(BackgroundBusLoop, self).loop()

    def loop(self):
        self.start()
        while not self.terminated:
            self.join(0.1)
