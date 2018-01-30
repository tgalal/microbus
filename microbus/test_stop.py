import microbus
import unittest


class CallbackFunc(object):
    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(args)

    def __len__(self):
        return len(self.calls)

    def __getitem__(self, item):
        return self.calls[item]


class TestBusStop(unittest.TestCase):
    def setUp(self):
        self.arrivingHandler = CallbackFunc()
        self.waitingPassengersClbk = CallbackFunc()
        self.stop = microbus.BusStop("aaa", self.arrivingHandler, self.waitingPassengersClbk)

    def test_wait_for_bus(self):
        data1 = "something"
        data2 = "something2"
        self.stop.wait_for_bus(data1)
        self.stop.wait_for_bus(data2)

        self.assertEqual([data1, data2], self.stop.departuringData)
        self.assertEqual(1, len(self.waitingPassengersClbk))
        self.assertEqual(0, len(self.arrivingHandler))

    def test_arrive(self):
        self.stop.wait_for_bus("a")
        self.stop.wait_for_bus("b")
        self.stop.arrive([1, 2])
        self.assertEqual(1, len(self.arrivingHandler))
        self.assertEqual([1, 2], self.arrivingHandler[0][1])

    def test_iter(self):
        self.stop.wait_for_bus("a")
        self.stop.wait_for_bus("b")
        for _ in self.stop:
            pass

        self.assertEqual(0, len(self.stop))

    def test_id(self):
        self.assertEqual(str, type(self.stop.id()))
        self.assertTrue(len(self.stop.id().rstrip()) > 0)

    def test_len(self):
        self.assertEqual(0, len(self.stop))
        self.stop.wait_for_bus("a")
        self.assertEqual(1, len(self.stop))
        self.stop.wait_for_bus("b")
        self.assertEqual(2, len(self.stop))
