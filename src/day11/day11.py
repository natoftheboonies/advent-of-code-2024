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
    0: [1],
    1: [2024],
    2024: [20, 24],
}


def split(rune):
    if not rune in rules:
        str_rune = str(rune)
        if len(str_rune) % 2 == 0:
            left = int(str_rune[: len(str_rune) // 2])
            right = int(str_rune[len(str_rune) // 2 :])
            rules[rune] = [left, right]
        else:
            rules[rune] = [rune * 2024]
    return rules[rune]


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().split()

    state_map = dict()
    for rune in data:
        state_map[int(rune)] = 1

    for i in range(75):
        next_state = dict()
        for rune in state_map:
            next_rune = split(rune)
            for nr in next_rune:
                next_state[nr] = next_state.get(nr, 0) + state_map[rune]
        state_map = next_state
        if i == 24:
            part1 = sum(state_map.values())
            logger.info(f"Part 1: {part1}")

    part2 = sum(state_map.values())
    logger.info(f"Part 2: {part2}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
