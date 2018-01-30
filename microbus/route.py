from microbus import BusStop


class BusRoute(object):
    def __init__(self, stops, name=""):
        assert type(stops) in (list, tuple), "%s is not list/type" % type(stops)
        self.name = name
        self._stops = stops[:]
        self._route_path = "_".join(map(lambda stop: stop.id(), stops))

    def __str__(self):
        return "%s: %s" % (self.name, self.route_path)

    def __getitem__(self, item):
        if type(item) is int:
            return self.stops[item]
        elif isinstance(item, slice):
            return BusRoute(self.stops[item], "sub_%s" % self.name)
        raise ValueError("Invalid index type: %s" % type(item))

    @property
    def stops(self):
        return self._stops

    @property
    def route_path(self):
        return self._route_path

    def __contains__(self, item):
        if type(item) is BusRoute:
            return item.route_path in self.route_path
        elif type(item) is BusStop:
            return item in self.stops

        return False

    def __len__(self):
        return len(self.stops)

    def __iter__(self):
        for stop in self.stops:
            yield stop
