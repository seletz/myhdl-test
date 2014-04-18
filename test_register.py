from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb
from myhdl import StopSimulation

from register import register, register_sync

PERIOD = 20
STEPS  = 100 * PERIOD

def test_register_sync():
    def register_test():

        ce     = Signal(bool(0))
        clk    = Signal(bool(0))
        q      = Signal(intbv(0))
        d      = Signal(intbv(0))

        reg = register_sync(q, d, ce, clk)

        DELAY = delay(PERIOD // 2)

        @always(DELAY)
        def clkgen():
            clk.next = not clk

        @always(clk.negedge)
        def monitor():
            print "CEv %d %s %s" % (ce, bin(q, 16), bin(d, 16))

        @instance
        def stimulus():
            for step in range(10):

                d.next = step

                if step % 2 == 0:
                    ce.next = not ce

                yield clk.negedge

                if ce == 0:
                    assert q != d

                if ce == 1:
                    assert q == d

            raise StopSimulation

        return reg, clkgen, monitor, stimulus

    tb = traceSignals(register_test)
    sim = Simulation(tb)
    sim.run()

if __name__ == '__main__':
    test_register_sync()
