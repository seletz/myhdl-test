from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb
from myhdl import StopSimulation

from mux2 import mux2

PERIOD = 20
STEPS  = 10

def test_mux():
    def mux_test():

        sel    = Signal(bool(0))
        q      = Signal(intbv(0))
        a      = Signal(intbv(0))
        b      = Signal(intbv(0))

        mux = mux2(q, a, b, sel)

        DELAY = delay(PERIOD // 2)

        @instance
        def stimulus():
            for step in range(STEPS):
                print "STEP %02d:" % step,

                a.next = step
                b.next = step << 8

                if step % 2 == 0:
                    sel.next = not sel

                yield DELAY
                print "%d q %s a %s b %s" % (sel, bin(q, 16), bin(a, 16), bin(b, 16))
                if sel % 2 == 0:
                    assert q == a
                else:
                    assert q == b

            raise StopSimulation

        return mux, stimulus

    tb = traceSignals(mux_test)
    sim = Simulation(tb)
    sim.run()

if __name__ == '__main__':
    test_mux()
