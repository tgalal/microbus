from microbus import BusAssignment, BusRoute
from microbus.bus import Bus
from zyklus import Zyklus


class BusLoop(Zyklus):
    def __init__(self):
        super(BusLoop, self).__init__()
        self.scheduledAssignments = []
        self.currentAssignment = None
        self.bus = Bus()

    def schedule(self, route):
        assert type(route) is BusRoute
        assignment = BusAssignment(self.bus, route)
        self.post(assignment)

    def ensure_postable(self, clbl):
        if super(BusLoop, self).ensure_postable(clbl):
            if isinstance(clbl, BusAssignment):
                route = clbl.route

                if self.currentAssignment is not None and route in self.currentAssignment:
                    # logger.info("Route in current assignment")
                    return False

                for assignment in self.scheduledAssignments:
                    if route in assignment.route:
                        # logger.info("Route in scheduled assignments")
                        return False

                self.scheduledAssignments.append(clbl)
                return True
            else:
                return True
        return False

    def remove_scheduled_assignment(self, assignment):
        self.scheduledAssignments.pop(self.scheduledAssignments.index(assignment))

    def exec_callable(self, clbl):
        if isinstance(clbl, BusAssignment):
            self.currentAssignment = clbl
            self.remove_scheduled_assignment(clbl)
            super(BusLoop, self).exec_callable(self.currentAssignment)
            self.currentAssignment = None
        else:
            super(BusLoop, self).exec_callable(clbl)
