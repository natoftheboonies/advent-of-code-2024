"""
Author: Nat with Darren's Template
Date: 2024-11-30

Solving https://adventofcode.com/2024/day/1

Part 1:

Part 2:

"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 1

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
        data = f.read().splitlines()
    left = list()
    right = list()
    for line in data:
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))

    left.sort()
    right.sort()
    sum_diff = 0
    for i in range(len(left)):
        diff = left[i] - right[i]
        sum_diff += abs(diff)

    logger.info(f"#1: {sum_diff}")

    total_sim = 0
    for i in range(len(left)):
        sim = right.count(left[i])
        if sim > 0:
            total_sim += sim * left[i]

    logger.info(f"#2: {total_sim}")
    # logger.debug(data)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
