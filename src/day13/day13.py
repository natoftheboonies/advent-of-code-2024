"""
Author: Nat with Darren's Template
Date: 2024-12-13

Solving https://adventofcode.com/2024/day/13
"""

import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2024
DAY = 13

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

"""
ax*a + bx*b = px
ay*a + by*b = py
b = (px - ax*a) / bx
ay*a*bx + by*(px - ax*a) = bx*py
ay*a*bx + by*px - by*ax*a = bx*py
ay*a*bx - by*ax*a = bx*py - by*px
a(ay*bx - by*ax) = bx*py - by*px
a = (bx*py - by*px) / (ay*bx - by*ax)
"""


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().split("\n\n")

    cost = 0
    for game in data:
        button_a, button_b, prize = game.strip().split("\n")
        ax, ay = map(int, (val.strip(",")[2:] for val in button_a.split()[2:]))
        logger.debug(f"ax: {ax}, ay: {ay}")
        bx, by = map(int, (val.strip(",")[2:] for val in button_b.split()[2:]))
        logger.debug(f"bx: {bx}, by: {by}")
        px, py = map(int, (val.strip(",")[2:] for val in prize.split()[1:]))
        logger.debug(f"px: {px}, py: {py}")
        px = px + 10000000000000
        py = py + 10000000000000
        a = (bx * py - by * px) / (ay * bx - by * ax)
        b = (px - ax * a) / bx
        logger.debug(f"a: {a}, b: {b}")
        if a.is_integer() and b.is_integer():
            cost += a * 3 + b
            logger.info(
                f"Winner: {int(a) * ax + int(b) * bx}, {int(a) * ay + int(b) * by}"
            )
    logger.info(f"Total cost: {int(cost)}")
    # logger.debug(data)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
