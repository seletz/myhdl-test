from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin, instances

from myhdl import delay, instance, always, always_seq, always_comb
from myhdl import StopSimulation

from alu import ALU, t_ALU_FUNCTION

PERIOD = 20
STEPS  = 10

WIDTH  = 8

BIN = lambda k: bin(k, WIDTH)

def test_alu():
    def alu_test():

        clk = Signal(bool(0))

        # flags
        n = Signal(bool(0))
        z = Signal(bool(0))
        o = Signal(bool(0))

        # a op b => q
        a   = Signal(intbv(0)[WIDTH:])
        b   = Signal(intbv(0)[WIDTH:])
        q   = Signal(intbv(0)[WIDTH:])

        # op
        af   = Signal(t_ALU_FUNCTION.ZERO)

        alu_inst = ALU(q, o, z, n, a, b, af, clk, width=WIDTH)

        DELAY = delay(PERIOD // 2)

        @always(DELAY)
        def clkgen():
            clk.next = not clk

        @instance
        def monitor():
            while True:
                print "a %s %s b %s => q %s" % (a, af, b, q)
                yield clk.negedge

        @instance
        def stimulus():

            def op(x, y, f):
                a.next = x
                b.next = y
                af.next = f
                yield delay(PERIOD // 4)
                yield clk.posedge

            yield op(2, 2, t_ALU_FUNCTION.A_PLUS_B)
            yield delay(PERIOD // 4)

            assert q == 4

            yield op(0, 0, t_ALU_FUNCTION.ZERO)
            yield delay(PERIOD // 4)

            assert q == 0

            yield op(1, 0, t_ALU_FUNCTION.NEG_A)
            yield delay(PERIOD // 4)

            assert q == 0xff

            yield op(42, 17, t_ALU_FUNCTION.A)
            yield delay(PERIOD // 4)

            assert q == 42

            yield op(42, 17, t_ALU_FUNCTION.B)
            yield delay(PERIOD // 4)

            assert q == 17

            yield op(0xaa, 0, t_ALU_FUNCTION.NOT_A)
            yield delay(PERIOD // 4)

            assert q == 0x55, "q %d %s %s" % (q, hex(q), BIN(q))

            yield op(0, 0x55, t_ALU_FUNCTION.NOT_B)
            yield delay(PERIOD // 4)

            assert q == 0xaa, "q %d %s %s" % (q, hex(q), BIN(q))

            yield DELAY
            yield DELAY
            raise StopSimulation

        return instances()

    tb = traceSignals(alu_test)
    sim = Simulation(tb)
    sim.run()

if __name__ == '__main__':
    test_alu()
