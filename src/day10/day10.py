"""
Author: Nat with Darren's Template
Date: 2024-12-10

Solving https://adventofcode.com/2024/day/10
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 10

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

    topo = list()
    for line in data:
        topo.append(tuple(map(int, list(line))))

    # logger.debug(topo)

    trailheads = list()
    for y, row in enumerate(topo):
        for x, cell in enumerate(row):
            if cell == 0:
                trailheads.append((x, y))
    logger.debug(trailheads)

    goal_count = 0
    part2_count = 0
    for trailhead in trailheads:
        queue = list()
        goals = list()
        visited = set()
        queue.append(trailhead)
        while queue:
            x, y = queue.pop(0)
            height = topo[y][x]
            # logger.debug(f"({x}, {y})")
            for dx, dy in ac.VectorDicts.DIRS.values():
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= len(topo[0]) or ny < 0 or ny >= len(topo):
                    continue
                if topo[ny][nx] != height + 1:
                    continue
                if (nx, ny) in visited:
                    continue
                if topo[ny][nx] == 9:
                    goals.append((nx, ny))
                    part2_count += 1

                queue.append((nx, ny))
        logger.debug(f"trailhead {trailhead} found {goals}")
        goal_count += len(set(goals))

    logger.info(f"Part 1: {goal_count}")
    logger.info(f"Part 2: {part2_count}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
