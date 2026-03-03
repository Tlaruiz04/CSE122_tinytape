# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset (even though ALU is combinational, keep protocol)
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test 3-bit ALU")

    # Helper to compute expected ALU output
    def alu_model(a, b, op):
        if op == 0:  # add
            tmp = a + b
        elif op == 1:  # sub
            # emulate 3-bit wrap-around subtraction
            tmp = (a - b) & 0x7
        elif op == 2:  # and
            tmp = a & b
        else:  # op == 3, xor
            tmp = a ^ b

        if op in (0, 1):
            # For add/sub we want 4 bits: {carry, result[2:0]}
            full = (a + b) if op == 0 else ((a - b) & 0xF)
            carry = (full >> 3) & 0x1
            res = full & 0x7
        else:
            carry = 0
            res = tmp & 0x7

        # uo_out[3:0] = {carry, res[2:0]}, upper bits zero
        return (carry << 3) | res

    # Exhaustive test over a, b in 0..7 and op in 0..3
    for op in range(4):
        for a in range(8):
            for b in range(8):
                ui_in = (op << 6) | (b << 3) | a
                dut.ui_in.value = ui_in

                # Wait one clock so combinational logic settles and is sampled
                await ClockCycles(dut.clk, 1)

                got = int(dut.uo_out.value)
                expected_low = alu_model(a, b, op)

                # Check lower 4 bits match, upper 4 bits are zero
                assert (got & 0xF) == expected_low, (
                    f"Mismatch for op={op}, a={a}, b={b}: "
                    f"expected low=0x{expected_low:x}, got low=0x{got & 0xF:x}"
                )
                assert (got >> 4) == 0, (
                    f"Upper bits not zero for op={op}, a={a}, b={b}: got 0x{got >> 4:x}"
                )
