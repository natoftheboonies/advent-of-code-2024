"""
Author: Nat with Darren's Template
Date: 2024-12-06

Solving https://adventofcode.com/2024/day/6
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 6

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

dirs = [ac.Vectors.S.value, ac.Vectors.E.value, ac.Vectors.N.value, ac.Vectors.W.value]


def explore(bounds, obstacles, guard, guard_idx):
    visited = set()
    visited.add(guard)
    turns = set()
    while True:
        dx, dy = dirs[guard_idx]

        new_pos = (guard[0] + dx, guard[1] + dy)
        # logger.debug(f"Guard: {guard}, New Pos: {new_pos}")
        if (
            new_pos[0] < 0
            or new_pos[0] >= bounds[0]
            or new_pos[1] < 0
            or new_pos[1] >= bounds[1]
        ):
            break
        if new_pos in obstacles:
            turn = (guard, guard_idx, new_pos)
            if turn in turns:
                # logger.debug(f"Looping: {turn}")
                return None
            turns.add(turn)
            guard_idx = (guard_idx + 1) % 4
            continue
        else:
            guard = new_pos
            visited.add(guard)
    return visited


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file

    obstacles = set()
    guard = None
    guard_idx = 0
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
        bounds = (len(data[0]), len(data))
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                if c == "#":
                    obstacles.add((x, y))
                elif c == "^":
                    guard = (x, y)

    part1 = explore(bounds, obstacles, guard, guard_idx)

    logger.debug(f"Part 1: {len(part1)}")
    # assert part1 == 4776

    part2 = 0
    for x, y in part1:
        if (x, y) == guard:
            continue
        new_obstacles = obstacles.copy()
        new_obstacles.add((x, y))
        detect_loop = explore(bounds, new_obstacles, guard, guard_idx)
        if detect_loop is None:
            part2 += 1

    logger.debug(f"Part 2: {part2}")
    # logger.debug(data)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
