"""
Author: Nat with Darren's Template
Date: 2024-12-15

Solving https://adventofcode.com/2024/day/15
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 15

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def print_state(robot, food, walls):
    max_y = max(y for x, y in walls)
    max_x = max(x for x, y in walls)
    x, y = robot
    for y_ in range(max_y + 1):
        for x_ in range(max_x + 1):
            if (x_, y_) == robot:
                print("@", end="")
            elif (x_, y_) in food:
                print("O", end="")
            elif (x_, y_) in walls:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


move_map = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        maze, moves = f.read().split("\n\n")
        moves = (move for move in moves.strip() if move != "\n")
        # logger.debug(moves)
        walls = set()
        food = set()
        for y, row in enumerate(maze.splitlines()):
            for x, cell in enumerate(row):
                if cell == "@":
                    robot = (x, y)
                elif cell == "O":
                    food.add((x, y))
                elif cell == "#":
                    walls.add((x, y))
    #     logger.debug(walls)
    # logger.debug(robot)
    for move in moves:
        # print_state(robot, food, walls)
        # print(f"Move {move}:")
        dx, dy = move_map[move]
        new_robot = (robot[0] + dx, robot[1] + dy)
        if new_robot in walls:
            continue
        if new_robot in food:
            # find the next empty space
            shift = new_robot
            while shift in food:
                shift = (shift[0] + dx, shift[1] + dy)
            if shift in walls:
                continue
            food.remove(new_robot)
            food.add(shift)
        robot = new_robot
    print_state(robot, food, walls)
    part1 = sum(100 * y + x for x, y in food)
    logger.info("Part 1: %s", part1)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
