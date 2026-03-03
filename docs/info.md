<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

My project is a simple 3-bit ALU that takes in 8 bits on input 3 bits for A, 3 for B, and 2 for select bits, and outputs a value based on the combo of input bits.
## How to test
DISCLAIMER: LLM was used to construct the testbench for this project, it created a testbench that checked if the output incremented every 100 clock cycles. All project.v code is my own.
The testbnech tests each part of the ALU by creating an ideal model of an ALU and compares my codes output with ideal expected results. To manually test, make sure to drive input to a value with a known output and compare the code with this value.

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
