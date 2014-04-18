from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb

from myhdl import toVerilog, toVHDL

def register_sync(q, d, ce, clk):
    """
    register -- a register with clock enable
    """

    @always(clk.posedge)
    def logic():
        if ce:
            q.next = d

    return logic

def register(q, d, ce):
    """
    register -- a register with clock enable
    """

    @always_comb
    def logic():
        if ce:
            q.next = d

    return logic

def to_hdl(f, width):
    ce  = Signal(bool(0))
    clk = Signal(bool(0))

    q   = Signal(intbv(0)[width:])
    d   = Signal(intbv(0)[width:])

    f(register_sync, q, d, ce, clk)
    f(register, q, d, ce)

if __name__ == '__main__':
    for f in (toVerilog, toVHDL):
        to_hdl(f, 16)

