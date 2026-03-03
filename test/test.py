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

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Give one extra cycle after releasing reset
    await ClockCycles(dut.clk, 1)

    dut._log.info("Check counter after reset")
    # After reset, the slow counter should start at 0
    assert int(dut.uo_out.value) == 0

    # Now check that uo_out increments every 100 clock cycles
    dut._log.info("Check that uo_out increments every 100 cycles")
    expected = 0
    for _ in range(5):
        await ClockCycles(dut.clk, 100)
        expected += 1
        assert int(dut.uo_out.value) == expected

    # Changing the other inputs should not affect the counter behavior
    dut._log.info("Change ui_in/uio_in and ensure counter keeps running")
    dut.ui_in.value = 123
    dut.uio_in.value = 42

    await ClockCycles(dut.clk, 100)
    expected += 1
    assert int(dut.uo_out.value) == expected
