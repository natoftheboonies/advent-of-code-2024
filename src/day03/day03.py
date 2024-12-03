"""
Author: Nat with Darren's Template
Date: 2024-12-03

Solving https://adventofcode.com/2024/day/3
"""

import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2024
DAY = 3

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read()

    # logger.debug(data)
    expr = re.compile(r"mul\(\d+,\d+\)")
    result = 0
    for inst in expr.finditer(data):
        a, b = map(int, inst.group()[4:-1].split(","))
        logger.debug(f"{inst.group()}: {a*b}")

        result += a * b
    logger.info("Part 1: %s", result)
    assert result == 168539636

    # part 2
    expr = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    result = 0
    do = True
    for inst in expr.finditer(data):
        if inst.group() == "do()":
            do = True
        elif inst.group() == "don't()":
            do = False
        elif do:
            a, b = map(int, inst.group()[4:-1].split(","))
            result += a * b
    logger.info("Part 2: %s", result)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
