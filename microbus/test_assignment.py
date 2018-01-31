from microbus.assignment import BusAssignment
import microbus
from microbus.bus import Bus
import unittest


class BusAssignmentTest(unittest.TestCase):
    def setUp(self):
        self.stop1 = microbus.BusStop("stop1")
        self.stop2 = microbus.BusStop("stop2")
        self.stop3 = microbus.BusStop("stop3")
        self.stops = [self.stop1, self.stop2, self.stop3]
        self.busRoute1 = microbus.BusRoute(self.stops, name="test")
        self.busRoute2 = self.busRoute1[::-1]
        self.bus = Bus(keep_prev=1)

    def test__contains(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        self.assertTrue(self.bus in assignment)
        self.assertTrue(self.busRoute1 in assignment)
        self.assertTrue(self.busRoute1[1:] in assignment)
        self.assertTrue(self.busRoute1[2:] in assignment)
        self.assertTrue(self.stop1 in assignment)
        self.assertTrue(self.stop2 in assignment)
        self.assertTrue(self.stop3 in assignment)
        self.assertFalse(microbus.BusStop("bla") in assignment)
        self.assertFalse(self.busRoute1[::-1] in assignment)
        self.assertFalse(self.busRoute1[::-1][1:] in assignment)

    def test_finished(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        self.assertFalse(assignment.finished)
        assignment()
        self.assertTrue(assignment.finished)

    def test_call(self):
        assignment = BusAssignment(self.bus, self.busRoute1)
        assignment()
        self.assertTrue(self.busRoute1 in self.bus.prev_routes)
        self.assertEqual(1, self.bus.completed_routes)

    def test_call_with_driver(self):
        assigned_trips = []

        def fulltrip_driver(trip):
            assigned_trips.append(trip)
            for _ in trip:
                pass

        def midtrip_driver(trip):
            assigned_trips.append(trip)
            next(trip)
            trip.close()

        def careless_driver(trip):
            assigned_trips.append(trip)
            next(trip)

        assignment = BusAssignment(self.bus, self.busRoute1, driver=fulltrip_driver)
        assignment()
        self.assertEqual(1, self.bus.completed_routes)
        self.assertEqual(1, len(assigned_trips))
        self.assertTrue(self.busRoute1 in self.bus.prev_routes)

        assignment = BusAssignment(self.bus, self.busRoute2, driver=midtrip_driver)
        assignment()
        self.assertEqual(1, self.bus.completed_routes)
        self.assertEqual(2, len(assigned_trips))
        self.assertTrue(self.busRoute2 in self.bus.prev_routes)

        assignment = BusAssignment(self.bus, self.busRoute1, driver=careless_driver)
        assignment()
        self.assertEqual(1, self.bus.completed_routes)
        self.assertEqual(3, len(assigned_trips))
        self.assertTrue(self.busRoute1 in self.bus.prev_routes)

        assignment = BusAssignment(self.bus, self.busRoute2, driver=fulltrip_driver)
        assignment()
        self.assertEqual(2, self.bus.completed_routes)
        self.assertEqual(4, len(assigned_trips))
        self.assertTrue(self.busRoute2 in self.bus.prev_routes)
