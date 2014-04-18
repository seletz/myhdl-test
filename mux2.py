from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb

from myhdl import toVerilog, toVHDL

def mux2(q, a, b, sel):
    """
    multiplexor
    """

    @always_comb
    def logic():
        if sel:
            q.next = b
        else:
            q.next = a

    return logic

def to_hdl(f, width):
    sel = Signal(bool(0))

    a   = Signal(intbv(0)[width:])
    b   = Signal(intbv(0)[width:])
    q   = Signal(intbv(0)[width:])

    f(mux2, q, a, b, sel)

if __name__ == '__main__':
    for f in (toVerilog, toVHDL):
        to_hdl(f, 16)
