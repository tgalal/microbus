import unittest
import microbus
from microbus.bus import Bus
from microbus.test_stop import CallbackFunc

class WaitForBusCallback(CallbackFunc):
    def __init__(self):
        super(WaitForBusCallback, self).__init__()
        self.stop = None

    def __call__(self, *args, **kwargs):
        super(WaitForBusCallback, self).__call__(*args, **kwargs)
        for item in args[0]:
            self.stop.wait_for_bus(item)

class BusTest(unittest.TestCase):
    def setUp(self):
        self.stop1ArrivingPassengersHandler = WaitForBusCallback()
        self.stop2ArrivingPassengersHandler = WaitForBusCallback()
        self.stop3ArrivingPassengersHandler = WaitForBusCallback()

        self.stop1Passengers = ['a', 'b', 'c']
        self.stop2Passengers = ['d', 'e', 'f']
        self.stop3Passengers = ['g', 'h', 'i']

        self.stop1 = microbus.BusStop("stop1", self.stop1ArrivingPassengersHandler)
        self.stop1ArrivingPassengersHandler.stop = self.stop1

        self.stop2 = microbus.BusStop("stop2", self.stop2ArrivingPassengersHandler)
        self.stop2ArrivingPassengersHandler.stop = self.stop2

        self.stop3 = microbus.BusStop("stop3", self.stop3ArrivingPassengersHandler)
        self.stop3ArrivingPassengersHandler.stop = self.stop3

        self.stops = [self.stop1, self.stop2, self.stop3]

        list(map(lambda p: self.stop1.wait_for_bus(p), self.stop1Passengers))
        list(map(lambda p: self.stop2.wait_for_bus(p), self.stop2Passengers))
        list(map(lambda p: self.stop3.wait_for_bus(p), self.stop3Passengers))

        self.busRoute = microbus.BusRoute("test", self.stops)
        self.bus = Bus()

    def test_schedule(self):
        self.bus.schedule(self.busRoute)
        self.bus.end()
        self.bus.standby()

        self.assertEqual(0, len(self.stop1.departuringData))
        self.assertEqual(0, len(self.stop2.departuringData))

        self.assertEqual(0, len(self.stop1ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop2ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop3ArrivingPassengersHandler))

        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop2Passengers + self.stop1Passengers, list(self.stop3ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop3Passengers + self.stop2Passengers + self.stop1Passengers, self.stop3.departuringData)

    def test_depart(self):
        gen = self.bus.depart(self.busRoute)
        stop, remainingRoute = next(gen)

        self.assertEqual(stop, self.stop1)
        self.assertEqual(2, len(remainingRoute))
        self.assertEqual(self.stop2, remainingRoute[0])
        self.assertEqual(self.stop3, remainingRoute[1])

        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop2)
        self.assertEqual(1, len(remainingRoute))
        self.assertEqual(self.stop3, remainingRoute[0])

        stop,remainingRoute = next(gen)
        self.assertEqual(stop, self.stop3)
        self.assertEqual(0, len(remainingRoute))


        try:
            next(gen)
            raise AssertionError()
        except StopIteration:
            pass

        self.assertEqual(0, len(self.stop1.departuringData))
        self.assertEqual(0, len(self.stop2.departuringData))

        self.assertEqual(0, len(self.stop1ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop2ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop3ArrivingPassengersHandler))

        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop2Passengers + self.stop1Passengers, list(self.stop3ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop3Passengers + self.stop2Passengers + self.stop1Passengers, self.stop3.departuringData)

    def test_board(self):
        passengers = self.bus.board(self.stop1)
        self.assertEqual(self.stop1Passengers, passengers)
        self.assertEqual(0, len(self.stop1))

    def test_unboard(self):
        self.bus.unboard(self.stop1Passengers[:], self.stop2)
        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][0]))

    def test_yield(self):
        standingBy = self.bus.standby2()
        next(standingBy)
        gen = standingBy.send(self.busRoute)

        stop, remainingRoute = next(gen)

        self.assertEqual(stop, self.stop1)
        self.assertEqual(2, len(remainingRoute))
        self.assertEqual(self.stop2, remainingRoute[0])
        self.assertEqual(self.stop3, remainingRoute[1])

        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop2)
        self.assertEqual(1, len(remainingRoute))
        self.assertEqual(self.stop3, remainingRoute[0])

        stop, remainingRoute = next(gen)
        self.assertEqual(stop, self.stop3)
        self.assertEqual(0, len(remainingRoute))

        try:
            next(gen)
            raise AssertionError()
        except StopIteration:
            pass

        self.assertEqual(0, len(self.stop1.departuringData))
        self.assertEqual(0, len(self.stop2.departuringData))

        self.assertEqual(0, len(self.stop1ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop2ArrivingPassengersHandler))
        self.assertEqual(1, len(self.stop3ArrivingPassengersHandler))

        self.assertEqual(self.stop1Passengers, list(self.stop2ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop2Passengers + self.stop1Passengers, list(self.stop3ArrivingPassengersHandler[0][0]))
        self.assertEqual(self.stop3Passengers + self.stop2Passengers + self.stop1Passengers, self.stop3.departuringData)



