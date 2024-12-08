"""
Author: Nat with Darren's Template
Date: 2024-12-08

Solving https://adventofcode.com/2024/day/8
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 8

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

    # logger.debug(data)
    bounds = (len(data[0]), len(data))

    signals = dict()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c != ".":
                signals[c] = signals.get(c, []) + [(x, y)]

    antinodes = set()
    harmonics = set()
    for coords in signals.values():
        for s1 in coords:
            for s2 in coords:
                if s1 == s2:
                    continue
                harmonics.add(s1)
                harmonics.add(s2)
                s1x, s1y = s1
                s2x, s2y = s2
                # calc point on s1 -> s2 line past s2 by distance from s1
                dx = s2x - s1x
                dy = s2y - s1y
                a1x = s2x + dx
                a1y = s2y + dy
                if a1x >= 0 and a1x < bounds[0] and a1y >= 0 and a1y < bounds[1]:
                    antinodes.add((a1x, a1y))
                a2x = s1x - dx
                a2y = s1y - dy
                if a2x >= 0 and a2x < bounds[0] and a2y >= 0 and a2y < bounds[1]:
                    antinodes.add((a2x, a2y))
                # resonant antinodes
                factor = 1
                while True:
                    a1x = s2x + dx * factor
                    a1y = s2y + dy * factor
                    if a1x < 0 or a1x >= bounds[0] or a1y < 0 or a1y >= bounds[1]:
                        break
                    harmonics.add((a1x, a1y))
                    factor += 1
                factor = 1
                while True:
                    a2x = s1x - dx * factor
                    a2y = s1y - dy * factor
                    if a2x < 0 or a2x >= bounds[0] or a2y < 0 or a2y >= bounds[1]:
                        break
                    harmonics.add((a2x, a2y))
                    factor += 1
    part1 = len(antinodes)
    logger.info("Part 1: %s", part1)
    part2 = len(harmonics)
    logger.info("Part 2: %s", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
