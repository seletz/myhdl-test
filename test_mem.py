from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb
from myhdl import StopSimulation

from mem import mem

PERIOD = 20
STEPS  = 10

WIDTH  = 8
DEPTH  = 16

BIN = lambda k: bin(k, WIDTH)

def test_mem():
    def mem_test():

        clk = Signal(bool(0))
        rnw = Signal(bool(1))

        di  = Signal(intbv(0)[WIDTH:])
        do  = Signal(intbv(0)[WIDTH:])
        a   = Signal(intbv(0)[WIDTH:])

        mem_inst = mem(do, di, a, rnw, clk, width=WIDTH, depth=DEPTH)

        DELAY = delay(PERIOD // 2)

        @always(DELAY)
        def clkgen():
            clk.next = not clk

        @instance
        def monitor():
            while True:
                print "%d MEM[%s] do %s di %s" % (rnw, BIN(a), BIN(do), BIN(di))
                yield DELAY

        @instance
        def stimulus():
            def write(byte, adr):
                a.next = adr
                di.next = byte
                yield clk.posedge

                rnw.next = 0
                yield clk.posedge

                rnw.next = 1
                yield clk.posedge

            for step in range(STEPS):
                yield write(step << 4, step)

            raise StopSimulation

        return mem_inst, clkgen, monitor, stimulus

    tb = traceSignals(mem_test)
    sim = Simulation(tb)
    sim.run()

if __name__ == '__main__':
    test_mem()
