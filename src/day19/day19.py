"""
Author: Nat with Darren's Template
Date: 2024-12-19

Solving https://adventofcode.com/2024/day/19
"""

import logging
import time
import aoc_common.aoc_commons as ac
import functools

YEAR = 2024
DAY = 19

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
        towels, patterns = f.read().split("\n\n")
        towels = set(towels.strip().split(", "))
        patterns = patterns.strip().split("\n")

    logger.debug(towels)
    logger.debug(patterns)
    count = 0

    @functools.cache
    def match(pattern):
        # logger.debug(f"Matching {pattern}")
        count = 0
        for towel in towels:
            if pattern.startswith(towel):
                # logger.debug(f"Matched {towel} with {pattern}")
                if towel == pattern:
                    count += 1
                count += match(pattern[len(towel) :])
        return count

    # match(patterns[2])
    # return
    all_possible = 0
    for i, pattern in enumerate(patterns):
        possible = match(pattern)
        if possible > 0:
            logger.debug(f"{i}: Matching {pattern}: {possible}")
            all_possible += match(pattern)
            count += 1

        else:
            logger.debug(f"{i}: Failed to match {pattern}")

    logger.info(count)
    logger.info(all_possible)  # not 811


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
