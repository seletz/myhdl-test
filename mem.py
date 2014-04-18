from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin

from myhdl import delay, instance, always, always_seq, always_comb

from myhdl import toVerilog, toVHDL

def mem(dout, din, addr, r_nwr, clk, width=8, depth=128):
    """
    memory
    """

    mem = [Signal(intbv(0)[width:]) for i in range(depth)]

    @always(clk.posedge)
    def write():
        if r_nwr == 0:
            mem[addr].next = din

    @always_comb
    def read():
        dout.next = mem[addr]

    return write, read


def to_hdl(f, width, depth):
    clk = Signal(bool(0))
    rnw = Signal(bool(0))

    di  = Signal(intbv(0)[width:])
    do  = Signal(intbv(0)[width:])
    a   = Signal(intbv(0)[width:])

    f(mem, do, di, a, rnw, clk, width=width, depth=depth)

if __name__ == '__main__':
    for f in (toVerilog, toVHDL):
        to_hdl(f, 16, 16)

