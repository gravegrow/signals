import unittest

from signals.connection import Connection
from signals.signal import Signal


class TestSignals(unittest.TestCase):
    def setUp(self) -> None:
        self.signal: Signal = Signal()
        self.addition_result = 0
        self.text = ""

    def add(self, x, y):
        self.addition_result = 0
        self.addition_result = x + y

    def add_kw(self, x=7, y=2):
        self.addition_result = 0
        self.addition_result = x + y

    def text_change(self):
        self.text = ""
        self.text = "changed"

    def test_connect_disconnect(self):
        self.signal.connect(self.add)
        self.assertEqual(self.signal.connections[0], Connection(self.add))

        self.signal.connect(self.add)
        self.assertEqual(len(self.signal.connections), 1)

        self.signal.disconnect(self.add)
        self.assertEqual(self.signal.connections, [])

    def test_emmit(self):
        self.signal.connect(self.add)
        self.signal.connect(self.text_change)
        self.signal.emit(12, -7)

        self.assertEqual(self.addition_result, 5)
        self.assertEqual(self.text, "changed")

    def test_emmit_kwargs(self):
        self.signal.connect(self.add_kw)
        self.signal.emit(2, 14, x=1)
        self.assertEqual(self.addition_result, 3)

        self.signal.emit(2, 14, x=1, y=-7)
        self.assertEqual(self.addition_result, -6)

    def test_emmit_args_kwargs(self):
        self.signal.connect(self.add_kw)
        self.signal.emit()
        self.assertEqual(self.addition_result, 9)

        self.signal.connect(self.add_kw)
        self.signal.emit(x=6, y=-2, z=13)
        self.assertEqual(self.addition_result, 4)

    def test_bind(self):
        self.signal.connect(self.add).bind(15, 11)
        self.signal.emit(5, 3)
        self.assertEqual(self.addition_result, 26)

    def test_bind_kw(self):
        self.signal.connect(self.add_kw).bind(x=7, y=2)
        self.signal.emit()
        self.assertEqual(self.addition_result, 9)


if __name__ == "__main__":
    unittest.main()
