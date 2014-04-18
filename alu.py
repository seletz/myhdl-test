
from random import randrange
from myhdl import Signal
from myhdl import intbv
from myhdl import traceSignals
from myhdl import Simulation

from myhdl import bin, instances

from myhdl import enum

from myhdl import delay, instance, always, always_seq, always_comb

from myhdl import toVerilog, toVHDL

t_ALU_FUNCTION = enum(
    "ZERO",
    "ONES",
    "A",
    "NEG_A",
    "A_PLUS_1",
    "B",
    "NEG_B",
    "B_PLUS_1",
    "A_PLUS_B",
    "NOT_A",
    "NOT_B",
    "A_AND_B",
    "A_OR_B",
    "A_XOR_B",
    )

def ALU(q, o, z, n, a, b, f, clk, width=16):
    """
    Simple ALU.

    See ARM System Aerchitecture "Introduction To Processor Design"
    """

    result = Signal(intbv(0)[width:])

    @always(clk.posedge)
    def alu_func():
        if f == t_ALU_FUNCTION.ZERO:
            result.next = 0
        elif f == t_ALU_FUNCTION.ONES:
            result.next = 2 ** width - 1
        elif f == t_ALU_FUNCTION.NEG_A:
            result.next = -a % 2 ** width
        elif f == t_ALU_FUNCTION.NEG_B:
            result.next = -b % 2 ** width
        elif f == t_ALU_FUNCTION.NOT_A:
            result.next = ~a
        elif f == t_ALU_FUNCTION.NOT_B:
            result.next = ~b
        elif f == t_ALU_FUNCTION.A:
            result.next = a
        elif f == t_ALU_FUNCTION.B:
            result.next = b
        elif f == t_ALU_FUNCTION.A_PLUS_1:
            result.next = a + 1
        elif f == t_ALU_FUNCTION.B_PLUS_1:
            result.next = b + 1
        elif f == t_ALU_FUNCTION.A_AND_B:
            result.next = a & b
        elif f == t_ALU_FUNCTION.A_OR_B:
            result.next = a | b
        elif f == t_ALU_FUNCTION.A_XOR_B:
            result.next = a ^ b
        elif f == t_ALU_FUNCTION.A_PLUS_B:
            result.next = a + b

    @always_comb
    def alu_status():
        q.next = result

        if result == 0:
            z.next = 1
        else:
            z.next = 0

        n.next = result[width - 1]

        # how to detect overflow?
        o.next = 0

    return instances()


def to_hdl(f, width):
    clk = Signal(bool(0))

    n = Signal(bool(0))
    z = Signal(bool(0))
    o = Signal(bool(0))

    q   = Signal(intbv(0)[width:])
    a   = Signal(intbv(0)[width:])
    b   = Signal(intbv(0)[width:])

    af   = Signal(t_ALU_FUNCTION.ZERO)

    f(ALU, q, o, z, n, a, b, af, clk, width=width)

if __name__ == '__main__':
    for f in (toVerilog, toVHDL):
        to_hdl(f, 16)

