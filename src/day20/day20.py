"""
Author: Nat with Darren's Template
Date: 2024-12-20

Solving https://adventofcode.com/2024/day/20
"""

import logging
import time
import aoc_common.aoc_commons as ac
import heapq

YEAR = 2024
DAY = 20

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

    base_maze = set()
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                base_maze.add((x, y))
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)

    assert start and end
    bound_x, bound_y = max(x for x, y in base_maze), max(y for x, y in base_maze)

    def run_maze():

        queue = []
        # cost, position
        heapq.heappush(queue, (0, start, [start]))
        shortest = dict()
        best_cost = 1000000000000
        while queue:
            cost, position, path = heapq.heappop(queue)
            if position == end:
                best_cost = min(best_cost, cost)
                return best_cost, path
            px, py = position
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                new_pos = (px + dx, py + dy)
                if (
                    new_pos[0] < 0
                    or new_pos[0] >= bound_x
                    or new_pos[1] < 0
                    or new_pos[1] >= bound_y
                ):
                    continue
                if new_pos in maze:
                    continue
                if new_pos not in shortest or shortest[new_pos] > cost + 1:
                    shortest[new_pos] = cost + 1
                    heapq.heappush(queue, (cost + 1, new_pos, path + [new_pos]))
        return -1, None
        # for y in range(bound):
        #     for x in range(bound):
        #         if (x, y) in maze:
        #             print("#", end="")
        #         elif (x, y) in path:
        #             print("O", end="")
        #         else:
        #             print(".", end="")
        #     print()

    maze = base_maze.copy()
    baseline_cost, _ = run_maze()
    # maze.remove((8, 1))
    # check_cost, _ = run_maze()
    # logger.debug("Check cost: %s", check_cost)
    # return

    threshold = 100
    visited = set()
    part1 = 0

    best_cost = baseline_cost
    for x, y in base_maze:
        if x == 0 or y == 0 or x == bound_x or y == bound_y:
            continue

        # logger.debug("Removing walls at %s, %s", x, y)
        # copy maze without this wall
        maze = base_maze.copy()
        maze.remove((x, y))
        visited.add((x, y))
        has_right = (x + 1, y) in maze
        has_down = (x, y + 1) in maze
        if not has_right and not has_down:
            cost, _ = run_maze()
            best_cost = min(best_cost, cost)
            if baseline_cost - cost >= threshold:
                part1 += 1
                logger.debug(
                    "cheat at x: %s, y: %s saves %s", x, y, baseline_cost - cost
                )
            # logger.debug("Single Cost: %s", cost)
        if has_right and not visited.__contains__((x - 1, y)):
            maze.remove((x + 1, y))
            cost, _ = run_maze()
            best_cost = min(best_cost, cost)
            maze.add((x + 1, y))
            if baseline_cost - cost >= threshold:
                part1 += 1
                logger.debug(
                    "cheat at x: %s, y: %s saves %s", x, y, baseline_cost - cost
                )
            # logger.debug("Right Cost: %s", cost)
        if has_down and not visited.__contains__((x, y - 1)):
            maze.remove((x, y + 1))
            cost, _ = run_maze()
            best_cost = min(best_cost, cost)
            maze.add((x, y + 1))
            if baseline_cost - cost >= threshold:
                part1 += 1
                logger.debug(
                    "cheat at x: %s, y: %s saves %s", x, y, baseline_cost - cost
                )
            # logger.debug("Down Cost: %s", cost)

    logger.debug("Best: %s", best_cost)
    logger.info("Part 1: %s", part1)  # not 1331


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
