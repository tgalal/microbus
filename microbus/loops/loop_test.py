import unittest
import microbus
from microbus.loops import loop

class BusLoopTest(unittest.TestCase):
    def setUp(self):
        self.busLoop = loop.BusLoop()

    def test_schedule(self):
        pass