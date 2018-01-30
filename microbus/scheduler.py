from zyklus import Zyklus
from microbus import BusRoute
from microbus.assignment import BusAssignment


class BusScheduler(object):
    def __init__(self, bus):
        self.bus = bus
        self.zyklus = Zyklus()

    def schedule(self, route):
        assert type(route) is BusRoute
        self.schedule_assignment(BusAssignment(self.bus, route))

    def schedule_assignment(self, assignment):
        self.zyklus.post(assignment)

    def run(self):
        self.zyklus.loop()

    def end(self):
        self.zyklus.terminate()
