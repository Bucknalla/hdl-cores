from amaranth import *
from math import log2, ceil

class UpCounter(Elaboratable):
    """
    A variable width up counter with a fixed limit, where width is generated based on bit requirement of the limit.

    Parameters
    ----------
    limit : int
        The value at which the counter overflows.

    Attributes
    ----------
    en : Signal, in
        The counter is incremented if ``en`` is asserted, and retains
        its value otherwise.
    ovf : Signal, out
        ``ovf`` is asserted when the counter reaches its limit.
    """
    def __init__(self, limit):
        self.limit = limit

        # Ports
        self.en  = Signal()
        self.ovf = Signal()

        # State
        self.width = ceil(log2(limit) + 1)
        self.count = Signal(self.width)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.ovf.eq(self.count == self.limit)

        with m.If(self.en):
            with m.If(self.ovf):
                m.d.sync += self.count.eq(0)
            with m.Else():
                m.d.sync += self.count.eq(self.count + 1)

        return m