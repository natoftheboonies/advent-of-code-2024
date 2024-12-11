"""
Author: Nat with Darren's Template
Date: 2024-12-11

Solving https://adventofcode.com/2024/day/11
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 11

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


rules = {
    "": ["1"],
    "0": ["1"],
    "1": ["2024"],
    "2024": ["20", "24"],
}


def split(rune):
    if not rune in rules:
        if len(rune) % 2 == 0:
            left = rune[: len(rune) // 2].lstrip("0")
            right = rune[len(rune) // 2 :].lstrip("0")
            rules[rune] = [left, right]
        else:
            replace = str(int(rune) * 2024)
            rules[rune] = [replace]
    return rules[rune]


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().split()
        # data = "125 17".split()
        # data = "0 1 10 99 999".split()
    # logger.debug(data)

    for _ in range(25):
        next_gen = list()
        for rune in data:
            next_rune = split(rune)
            next_gen.extend(next_rune)
        # logger.debug(next_gen)
        data = next_gen

    logger.debug("len rules: %d", len(rules))
    logger.info(f"Part 1: {len(data)}")  # not 165428


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
