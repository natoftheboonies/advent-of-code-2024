"""
Author: Nat with Darren's Template
Date: 2024-12-21

Solving https://adventofcode.com/2024/day/21
"""

import logging
import time
import aoc_common.aoc_commons as ac
from collections import deque
from functools import cache

YEAR = 2024
DAY = 21

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

numeric_keypad = (("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), (None, "0", "A"))
direction_keypad = ((None, "^", "A"), ("<", "v", ">"))
directions = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}
directions = {v: k for k, v in directions.items()}


@cache
def find_shortest(c, robot, key):
    visited = dict()
    visited[robot] = 0
    state = (robot, [])
    q = deque([state])
    while q:
        robot, path = q.popleft()
        # logger.debug(f"Robot: {robot}, path: {path}")
        x, y = robot
        if key[y][x] == c:
            return (x, y), path + ["A"]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(key[0]) and 0 <= ny < len(key):
                if key[ny][nx] is not None and (nx, ny) not in visited:
                    visited[(nx, ny)] = visited[(x, y)] + 1
                    q.append(((nx, ny), path + [directions[(dx, dy)]]))
    logger.error(f"Could not find {c} from {robot}")
    return None


def find_moves(sequence, robot, key):
    all_moves = []
    for c in sequence:
        robot, moves = find_shortest(c, robot, key)
        # logger.debug(f"Robot1: {robot1}, moves: {moves}")
        all_moves.extend(moves)
    return all_moves


def main():
    puzzle = locations.input_file
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
        assert len(data) == 5

    start1 = (2, 3)
    assert numeric_keypad[start1[1]][start1[0]] == "A"
    start2 = (2, 0)
    assert direction_keypad[start2[1]][start2[0]] == "A"

    for code in data:
        robot1_moves = find_moves(code, start1, numeric_keypad)
        robot2_moves = find_moves(robot1_moves, start2, direction_keypad)
        robot3_moves = find_moves(robot2_moves, start2, direction_keypad)
        multiplier = "".join(n for n in code if n.isdigit())
        result = len(robot3_moves) * int(multiplier)
        logger.debug(f"{code}: {len(robot3_moves)} * {multiplier} = {result}")


# todo: find all the shortest paths, because entering them is not always the shortest path


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
