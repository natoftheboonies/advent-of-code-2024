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


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
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
    heapq.heappush(queue, (0, start, (1, 0), [(1, 0)]))
    shortest = dict()
    good_seats = set()
    best_cost = 1000000000000
    while queue:
        cost, position, heading, path = heapq.heappop(queue)
        if position == end:
            best_cost = min(best_cost, cost)
            if best_cost == cost:
                good_seats.update(path)

            # break
        # try continuing forward
        forward = (position[0] + heading[0], position[1] + heading[1])
        # try turning left
        turnleft = (heading[1], -heading[0])  # 0, 1 -> 1, 0 -> 0, -1 -> -1, 0
        left = (position[0] + turnleft[0], position[1] + turnleft[1])
        # try turning right
        turnright = (-heading[1], heading[0])
        right = (position[0] + turnright[0], position[1] + turnright[1])

        for add_cost, pos, head in (
            (1, forward, heading),
            (1001, left, turnleft),
            (1001, right, turnright),
        ):
            if pos in maze:
                continue

            # if we haven't been here or we have but it was more expensive
            if not (pos, head) in shortest or shortest[(pos, head)] >= cost + add_cost:
                shortest[(pos, head)] = cost + add_cost
                heapq.heappush(queue, (cost + add_cost, pos, head, path + [pos]))
    logger.info("Part 1: %s", best_cost)
    logger.info("Part 2: %s", len(good_seats))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
