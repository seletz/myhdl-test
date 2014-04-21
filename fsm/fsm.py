from random import randrange
from myhdl import Signal, ResetSignal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation
from myhdl import StopSimulation

from myhdl import bin
from myhdl import enum
from myhdl import instances

from myhdl import delay, instance, always, always_seq, always_comb

from myhdl import toVerilog, toVHDL

_states = "START ONE_OK TWO_OK THREE_OK FOUR_OK ERROR OPEN".split()
t_STATE = enum(*_states)

def fsm(q, state_out, d, reset, clk):
    """
    Simple digital lock example.

    Combination:

    1, 2, 3, 4

    @param d(3..0):   INPUT (combination)
    @param q(1..0):   OUTPUT q(0) open/close state, q(1) error signal

    States:

    START, ONE_OK, TWO_OK, THREE_OK, FOUR_OK, ERROR, OPEN

    """
    state = Signal(t_STATE.START)

    @always_comb
    def fsm_comb():
        state_out.next = state

    #@always_comb
    #def fsm_reset():
        #if reset == 0:
            #state.next = t_STATE.START

    @always_seq(clk.posedge, reset=reset)
    def fsm_seq():
        print "fsm:  S %s, d %d" % (state, d)
        if state == t_STATE.START:
            if d == 1:
                state.next = t_STATE.ONE_OK
            else:
                q.next = 2
                state.next = t_STATE.ERROR

        elif state == t_STATE.ONE_OK:
            if d == 2:
                state.next = t_STATE.TWO_OK
            else:
                q.next = 2
                state.next = t_STATE.ERROR

        elif state == t_STATE.TWO_OK:
            if d == 3:
                state.next = t_STATE.THREE_OK
            else:
                q.next = 2
                state.next = t_STATE.ERROR

        elif state == t_STATE.THREE_OK:
            if d == 4:
                state.next = t_STATE.OPEN
                q.next = 1
            else:
                q.next = 2
                state.next = t_STATE.ERROR

        elif state == t_STATE.OPEN:
            q.next = 1

        elif state == t_STATE.ERROR:
            state.next = t_STATE.START
            q.next = 0

    return instances()

def test_fsm():
    PERIOD = 20

    DELAY   = delay(PERIOD // 2)
    DELAY2  = delay(PERIOD // 4)

    def test_fsm():
        clk     = Signal(bool(0))
        #reset   = Signal(bool(1))
        reset   = ResetSignal(bool(1), active=0, async=True)

        d   = Signal(intbv(0)[4:])
        q   = Signal(intbv(0)[2:])

        s   = Signal(t_STATE.START)

        dut = fsm(q, s, d, reset, clk)

        @always(DELAY)
        def clkgen():
            clk.next = not clk

        @instance
        def monitor():
            while True:
                print "O%d E%d" % (q(0), q(1))
                yield clk.negedge

        @instance
        def stimulus():
            def rst():
                yield delay(2)
                reset.next = 0
                yield delay(2)
                reset.next = 1

            def punch(val):
                #yield delay(2)
                d.next = val
                yield delay(2)

            yield rst()

            yield punch(1)
            yield clk.posedge

            yield punch(2)
            yield clk.posedge

            yield punch(3)
            yield clk.posedge

            yield punch(4)
            yield clk.posedge

            yield rst()

            yield punch(1)
            yield clk.posedge

            yield DELAY
            yield DELAY
            yield DELAY
            raise StopSimulation

        return instances()

    tb = traceSignals(test_fsm)
    sim = Simulation(tb)
    sim.run()

def to_hdl(f, *args, **kw):
    clk     = Signal(bool(0))
    # reset   = Signal(bool(0))
    reset   = ResetSignal(bool(1), active=0, async=True)

    d   = Signal(intbv(0)[4:])
    q   = Signal(intbv(0)[2:])

    s   = Signal(t_STATE.START)

    f(fsm, q, s, d, reset, clk)

if __name__ == '__main__':
    test_fsm()
    for f in (toVerilog, toVHDL):
        to_hdl(f)

