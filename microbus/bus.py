import logging
logger = logging.getLogger(__name__)


class SimultaneousRoutesException(Exception):
    pass


class Bus(object):
    def __init__(self, keep_prev=0):
        super(Bus, self).__init__()
        self._prev_routes = [None] * keep_prev
        self.current_route = None
        self._completed_routes = 0

    @property
    def prev_routes(self):
        return self._prev_routes

    @property
    def completed_routes(self):
        return self._completed_routes

    def depart(self, route):
        if self.current_route is not None:
            raise SimultaneousRoutesException("Can't depart 2 routes using same bus")
        else:
            self.add_to_history(route)
            return self._depart(route)

    def add_to_history(self, route):
        if len(self.prev_routes):
            self._prev_routes.pop()
            self._prev_routes.insert(0, route)

    def _depart(self, route):
        if self.current_route is not None:
            raise SimultaneousRoutesException()
        self.current_route = route
        # logger.debug("Deparing route %s" % route)
        onboard = []
        try:
            while len(self.current_route):
                stop = self.current_route[0]
                # logger.debug("Arrived at %s" % stop)
                curr_stop = stop
                self.unboard(onboard, curr_stop)
                onboard = []
                if stop is not self.current_route[-1]:
                    onboard = self.board(curr_stop)
                self.current_route = self.current_route[1:]
                yield (stop, self.current_route)
        finally:
            if not len(self.current_route):
                self._completed_routes += 1
            self.current_route = None

    def board(self, stop):
        # logger.debug("Boarding at %s " % self.curr_stop)
        passengers = []
        for p in stop:
            passengers.append(p)
        return passengers
        # print(self.onBoard)

    def unboard(self, passengers, stop):
        # logger.debug("Unboarding at %s " % self.curr_stop)
        if len(passengers):
            stop.arrive(passengers)

# class Bus(object):
#     def __init__(self):
#         super(Bus, self).__init__()
#         self._onboard = []
#         self._remaining_route = None
#         self._curr_stop = None
#
#     @property
#     def curr_stop(self):
#         return self._curr_stop
#
#     @property
#     def remaining_route(self):
#         return self._remaining_route
#
#     def depart(self, route):
#         if self.remaining_route is not None:
#             raise ValueError("Can't depart to routes at once")
#         self._remaining_route = route
#         # logger.debug("Deparing route %s" % route)
#
#         while len(self.remaining_route):
#             stop = self.remaining_route[0]
#             # logger.debug("Arrived at %s" % stop)
#             self._curr_stop = stop
#             self.unboard()
#             if stop is not self.remaining_route[-1]:
#                 self.board()
#             self._remaining_route = self.remaining_route[1:]
#         self._curr_stop=None
#         self._remaining_route = None
#
#     def board(self):
#         # logger.debug("Boarding at %s " % self.curr_stop)
#         for p in self.curr_stop:
#             self._onboard.append(p)
#         # print(self.onBoard)
#
#     def unboard(self):
#         # logger.debug("Unboarding at %s " % self.curr_stop)
#         if len(self._onboard):
#             toUnboard = self._onboard
#             self._onboard = []
#             self.curr_stop.arrive(toUnboard)
