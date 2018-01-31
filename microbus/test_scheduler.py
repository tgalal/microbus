from microbus.scheduler import BusScheduler
from microbus.assignment import BusAssignment
import time
import microbus
from microbus.bus import Bus
import threading
import unittest


class BusSchedulerTest(unittest.TestCase):
    def setUp(self):
        self.stop1 = microbus.BusStop("stop1")
        self.stop2 = microbus.BusStop("stop2")
        self.stop3 = microbus.BusStop("stop3")
        self.stops = [self.stop1, self.stop2, self.stop3]
        self.busRoute1 = microbus.BusRoute(self.stops, "test")
        self.busRoute2 = self.busRoute1[::-1]
        self.bus = Bus(keep_prev=2)
        self.scheduler = BusScheduler(self.bus)

    def tearDown(self):
        self.scheduler.end()

    def exec_scheduler_and_return(self, timeout=0.1):
        t = threading.Thread(target=self.scheduler.run)
        t.start()
        time.sleep(timeout)
        return t

    def test_schedule(self):
        # it should exec scheduled routes in order
        self.scheduler.schedule(self.busRoute1)
        self.scheduler.schedule(self.busRoute2)
        self.exec_scheduler_and_return()
        self.assertEqual(2, self.bus.completed_routes)
        self.assertEqual([self.busRoute2, self.busRoute1], self.bus.prev_routes)

    def test_schedule_with_driver(self):
        def drive_mid(trip):
            next(trip)

        def drive(trip):
            for _ in trip:
                pass

        def cancel_trip_drive(trip):
            trip.close()

        def cancel_mid_trip_drive(trip):
            next(trip)
            trip.close()

        self.scheduler.schedule(self.busRoute1, driver=drive)
        self.scheduler.schedule(self.busRoute2, driver=cancel_mid_trip_drive)
        self.scheduler.schedule(self.busRoute1, driver=cancel_trip_drive)
        self.scheduler.schedule(self.busRoute2, driver=drive)
        self.scheduler.schedule(self.busRoute2, driver=drive_mid)
        self.scheduler.schedule(self.busRoute2, driver=drive)
        self.exec_scheduler_and_return()
        self.assertEqual(3, self.bus.completed_routes)
        self.assertEqual([self.busRoute2, self.busRoute2], self.bus.prev_routes)

    def test_run(self):
        self.scheduler.schedule(self.busRoute1)
        self.scheduler.schedule(self.busRoute2)
        self.exec_scheduler_and_return()
        self.assertEqual(2, self.bus.completed_routes)

    def test_end(self):
        t = self.exec_scheduler_and_return()
        self.scheduler.end()
        time.sleep(0.1)
        self.assertFalse(t.isAlive())

    def test_schedule_assignment(self):
        self.scheduler.schedule_assignment(BusAssignment(self.bus, self.busRoute1))
        self.exec_scheduler_and_return()
        self.assertTrue(self.busRoute1 in self.bus.prev_routes)
