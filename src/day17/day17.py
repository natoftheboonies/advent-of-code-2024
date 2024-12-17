"""
Author: Nat with Darren's Template
Date: 2024-12-17

Solving https://adventofcode.com/2024/day/17
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 17

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def run_program(reg, program):
    def combo(operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return reg[0]
        elif operand == 5:
            return reg[1]
        elif operand == 6:
            return reg[2]
        else:
            logger.error("Invalid combo operand: %d", operand)
            assert False  # invalid operand

    output = []
    ip = 0
    while ip < len(program):
        op = program[ip]
        # logger.debug("ip=%d, op=%s, reg=%s", ip, op, reg)
        opcode, operand = op
        if opcode == 0:  # adv
            reg[0] = reg[0] // (2 ** combo(operand))
        elif opcode == 1:  # bxl
            reg[1] = reg[1] ^ operand
        elif opcode == 2:  # bst
            reg[1] = combo(operand) % 8
        elif opcode == 3:  # jnz
            assert operand % 2 == 0
            if reg[0] != 0:
                ip = operand // 2
                continue
        elif opcode == 4:  # bxc
            reg[1] = reg[1] ^ reg[2]
        elif opcode == 5:  # out
            output.append(combo(operand) % 8)
        elif opcode == 6:  # bdv
            reg[1] = reg[0] // (2 ** combo(operand))
        elif opcode == 7:  # cdv
            reg[2] = reg[0] // (2 ** combo(operand))
        ip += 1
    logger.debug("output=%s", output)
    # not 7,7,7,7,7,7,7,7,7
    return output


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read()
        registers, program = data.split("\n\n")
        registers = registers.splitlines()
        program = tuple(map(int, program.strip().split(": ")[1].split(",")))
        ops = [(program[i], program[i + 1]) for i in range(0, len(program), 2)]
        assert len(program) % 2 == 0
        reg = [int(line.split(": ")[1]) for line in registers]
        logger.debug("reg=%s, prog=%s", reg, ops)
        output = run_program(reg, ops)
        logger.info("Part 1: %s", ",".join(map(str, output)))

    # logger.debug(data)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
