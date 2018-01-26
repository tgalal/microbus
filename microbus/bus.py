import logging
import zyklus
import threading
import microbus
logger = logging.getLogger(__name__)


class Bus(object):
    def __init__(self):
        super(Bus, self).__init__()
        self.zyklus = zyklus.Zyklus()
        self.thread = None

    def schedule(self, route):
        self.zyklus.post(lambda: [_ for _ in self.depart(route)])

    def standby2(self):
        while True:
            route = yield
            assert isinstance(route, microbus.BusRoute)
            yield self.depart(route)

    def standby(self, background=False):
        if background:
            self.thread = threading.Thread(target=self.zyklus.loop)
            self.thread.start()
        else:
            self.zyklus.loop()

    def join(self):
        if self.thread is not None:
            self.thread.join()

    def end(self):
        self.zyklus.terminate()

    def depart(self, route):
        remaining_route = route
        # logger.debug("Deparing route %s" % route)
        onboard = []
        while len(remaining_route):
            stop = remaining_route[0]
            # logger.debug("Arrived at %s" % stop)
            curr_stop = stop
            self.unboard(onboard, curr_stop)
            onboard = []
            if stop is not remaining_route[-1]:
                onboard = self.board(curr_stop)
            remaining_route = remaining_route[1:]
            yield (stop, remaining_route)

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
