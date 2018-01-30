import microbus
import unittest


class BusRouteTest(unittest.TestCase):
    def setUp(self):
        self.stop1 = microbus.BusStop("stop1")
        self.stop2 = microbus.BusStop("stop2")
        self.stop3 = microbus.BusStop("stop3")
        self.stops = [self.stop1, self.stop2, self.stop3]
        self.busRoute = microbus.BusRoute(self.stops, "test")

    def test__get__item(self):
        self.assertEqual(self.stop2, self.busRoute[1])
        self.assertEqual([self.stop2, self.stop3], self.busRoute[1:].stops)
        self.assertEqual(self.stops[::-1], self.busRoute[::-1].stops)

    def test_routePath(self):
        route_path = "_".join(map(lambda s: s.id(), self.busRoute))
        self.assertEqual(route_path, self.busRoute.route_path)

    def test__contains__(self):
        for s in self.stops:
            self.assertTrue(s in self.busRoute)

        self.assertTrue(microbus.BusRoute([self.stop1, self.stop2]) in self.busRoute)
        self.assertTrue(microbus.BusRoute([self.stop2, self.stop3]) in self.busRoute)
        self.assertFalse(microbus.BusRoute([self.stop1, self.stop3]) in self.busRoute)
        self.assertFalse(microbus.BusRoute([self.stop2, self.stop1]) in self.busRoute)
        self.assertFalse(microbus.BusRoute([self.stop3, self.stop2]) in self.busRoute)
        self.assertFalse(microbus.BusRoute([self.stop3, self.stop1]) in self.busRoute)

    def test___len__(self):
        self.assertEqual(3, len(self.busRoute))

    def test__iter__(self):
        for s in self.busRoute:
            self.stops.pop(self.stops.index(s))
        self.assertEqual(0, len(self.stops))
