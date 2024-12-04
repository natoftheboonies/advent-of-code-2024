"""
Author: Nat with Darren's Template
Date: 2024-12-04

Solving https://adventofcode.com/2024/day/4
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 4

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def search(data, x, y):
    matches = 0
    for dx, dy in dirs:
        for i, c in enumerate("XMAS"):
            nx, ny = x + dx * i, y + dy * i
            if nx < 0 or ny < 0 or nx >= len(data[0]) or ny >= len(data):
                break
            if data[ny][nx] != c:
                break
        else:
            matches += 1
    return matches


opposite_dirs = [((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

""""
S S
 A
M M

M S
 A
M S

"""


def search2(data, x, y):
    pair = set("MS")
    for dir_pair in opposite_dirs:
        check_pair = set()
        for dir in dir_pair:

            dx, dy = dir
            if (
                x + dx < 0
                or y + dy < 0
                or x + dx >= len(data[0])
                or y + dy >= len(data)
            ):
                break
            check_pair.add(data[y + dy][x + dx])

        if check_pair != pair:
            break
    else:
        return 1
    return 0


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)
    result = 0
    result2 = 0
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "X":
                # search!
                result += search(data, x, y)
            if c == "A":
                result2 += search2(data, x, y)

    logger.debug(f"Part 1: {result}")
    logger.debug(f"Part 2: {result2}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
