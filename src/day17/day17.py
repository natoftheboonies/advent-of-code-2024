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
        opcode = program[ip]
        operand = program[ip + 1]
        if opcode == 0:  # adv
            reg[0] = reg[0] >> combo(operand)
        elif opcode == 1:  # bxl
            reg[1] = reg[1] ^ operand
        elif opcode == 2:  # bst
            reg[1] = combo(operand) % 8
        elif opcode == 3:  # jnz
            if reg[0] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            reg[1] = reg[1] ^ reg[2]
        elif opcode == 5:  # out
            output.append(combo(operand) % 8)
        elif opcode == 6:  # bdv
            reg[1] = reg[0] >> combo(operand)
        elif opcode == 7:  # cdv
            reg[2] = reg[0] >> combo(operand)
        ip += 2
    return output


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read()
    registers, program = data.split("\n\n")
    registers = registers.splitlines()
    program = list(map(int, program.strip().split(": ")[1].split(",")))
    assert len(program) % 2 == 0
    reg = [int(line.split(": ")[1]) for line in registers]
    output = run_program(reg, program)
    logger.info("Part 1: %s", ",".join(map(str, output)))

    # time to find a teacher :)
    # part 2 credit: https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2gfogr/
    # recursively look for a value of reg[0] that will make the program output the sub_program
    def find_reg_a(sub_program):
        test_a = 0 if len(sub_program) == 1 else 8 * find_reg_a(sub_program[1:])
        while True:
            reg = [test_a, 0, 0]
            output = run_program(reg, program)
            if output == sub_program:
                return test_a
            test_a += 1

    reg_a = find_reg_a(program)
    logger.info("Part 2: %s", reg_a)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
