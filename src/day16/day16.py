"""
Author: Nat with Darren's Template
Date: 2024-12-16

Solving https://adventofcode.com/2024/day/16
"""

import logging
import time
import aoc_common.aoc_commons as ac
import heapq

YEAR = 2024
DAY = 16

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # E, S, W, N


def main():
    puzzle = locations.input_file
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)
    maze = set()
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                maze.add((x, y))
            elif char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
    logger.debug("start: %s, end %s", start, end)
    queue = []
    # cost, position, heading
    heapq.heappush(queue, (0, start, (0, 1)))
    shortest = dict()
    while queue:
        cost, position, heading = heapq.heappop(queue)
        state = (position, heading)

        if state in shortest:
            if shortest[state] <= cost:
                continue
            else:
                shortest[state] = cost
        if position == end:
            logger.info("Found end at %s", cost)
            break
        # try continuing forward
        forward = (position[0] + heading[0], position[1] + heading[1])
        if forward not in maze:
            heapq.heappush(queue, (cost + 1, forward, heading))
        # try turning left
        left = (heading[1], -heading[0])  # 0, 1 -> 1, 0 -> 0, -1 -> -1, 0
        heapq.heappush(queue, (cost + 1000, position, left))
        # try turning right
        right = (-heading[1], heading[0])
        heapq.heappush(queue, (cost + 1000, position, right))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
