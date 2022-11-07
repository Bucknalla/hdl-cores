from amaranth.sim import Simulator
from main import *
import unittest
from pathlib import Path

class UpCounterTest(unittest.TestCase):
    def test_simple(self):

        limit = 15
        dut = UpCounter(limit)
        
        def bench():
            # Disabled counter should not overflow.
            yield dut.en.eq(0)
            for _ in range(limit):
                yield
                self.assertEqual((yield dut.ovf), 0)

            # Once enabled, the counter should overflow in limit number of cycles.
            yield dut.en.eq(1)
            for _ in range(limit):
                yield
                self.assertEqual((yield dut.ovf), 0)
            yield
            self.assertEqual((yield dut.ovf), 1)

            # The limit should clear in one cycle.
            yield
            self.assertEqual((yield dut.ovf), 0)

        sim = Simulator(dut)
        sim.add_clock(1e-6)
        sim.add_sync_process(bench)
        with sim.write_vcd(f"{Path(__name__).resolve().stem}.vcd"):
            sim.run()

            