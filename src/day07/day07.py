"""
Author: Nat with Darren's Template
Date: 2024-12-07

Solving https://adventofcode.com/2024/day/7
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 7

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def check_eq(expected, head, tail):
    if not tail:
        if head == expected:
            return True
    if head > expected or not tail:
        return False
    return check_eq(expected, head + tail[0], tail[1:]) or check_eq(
        expected, head * tail[0], tail[1:]
    )


def check_eq2(expected, head, tail, oper):
    if not tail:
        if head == expected:
            logger.debug(f"Found: {head} with {oper}")
            return True
    if head > expected or not tail:
        return False
    return (
        check_eq2(expected, head + tail[0], tail[1:], oper + "+")
        or check_eq2(expected, head * tail[0], tail[1:], oper + "*")
        or check_eq2(
            expected, int(str(head) + str(tail[0])), tail[1:], oper + "c"
        )  # Concatenate),
    )


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)
    sum_valid = 0
    sum2_valid = 0
    for line in data:
        left, right = line.split(": ")
        left = int(left)
        seq = tuple(map(int, right.split()))
        logger.debug(f"{left}, {seq}")
        if check_eq(left, seq[0], seq[1:]):
            sum_valid += left
        if check_eq2(left, seq[0], seq[1:], ""):
            logger.debug(f"Part 2 ok: {left}")
            sum2_valid += left

    logger.info(f"Part 1: {sum_valid}")
    logger.info(f"Part 2: {sum2_valid}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
