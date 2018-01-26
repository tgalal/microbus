import microbus


class BusAssignment(object):
    def __init__(self, bus, route):
        self.bus = bus
        self.route = route
        self.finished = False

    def __contains__(self, item):
        if isinstance(item, microbus.Bus):
            return self.bus == item

        if isinstance(item, microbus.BusRoute):
            if self.finished:
                return False
            if self.bus.remainingRoute is None:
                return item in self.route
            return item in self.bus.remainingRoute
        return False

    def __call__(self, *args, **kwargs):
        self.bus.depart(self.route)
        self.finished = True
