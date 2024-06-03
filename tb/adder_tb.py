# adder_tb.py (simple)

import cocotb
from cocotb.triggers import FallingEdge, Timer

@cocotb.test()
async def test(dut):
    for a in range(16):
        for b in range(16):
            for c in range (2):
                dut.a.value = a
                dut.b.value = b
                dut.c.value = c
                q = a + b + c
                await Timer(2, units="ns")
                assert dut.q.value == q, f"dut.q: {dut.q.value} does not match expected q: {q}"
