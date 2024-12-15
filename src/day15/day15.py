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


def print_state_part2(robot, food, walls):
    max_y = max(y for x, y in walls)
    max_x = max(x for x, y in walls)
    for y_ in range(max_y + 1):
        for x_ in range(max_x + 1):
            if (x_, y_) == robot:
                print("@.", end="")
            elif (x_, y_) in food:
                print("[]", end="")
            elif (x_, y_) in walls:
                print("##", end="")
            elif (x_ - 1, y_) not in walls | food | {robot}:
                print(".", end="")
        print()
    print()


move_map = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def part1(maze, moves):

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
    # print_state(robot, food, walls)
    part1 = sum(100 * y + x for x, y in food)
    logger.info("Part 1: %s", part1)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        maze, moves = f.read().split("\n\n")
        moves = (move for move in moves.strip() if move != "\n")
        # logger.debug(moves)
    # part1(maze, moves)

    # part2
    walls = set()
    food = set()
    for y, row in enumerate(maze.splitlines()):
        for x, cell in enumerate(row):
            if cell == "@":
                robot = (x * 2, y)
            elif cell == "O":
                food.add((x * 2, y))
            elif cell == "#":
                walls.add((x * 2, y))
    print_state_part2(robot, food, walls)
    # walls and food store left-side coordinates
    assert all((x + 1, y) not in walls | food for x, y in food | walls | {robot})

    def try_move(candidate, direction, blocks_to_move):
        logger.debug(
            "Trying to move to %s in %s with %s", candidate, direction, blocks_to_move
        )
        if direction[0] == -1 and (candidate[0] - 1, candidate[1]) in walls:
            # case "##<."
            return False, blocks_to_move
        if direction[0] == 1 and candidate in walls:
            # case ".>##"
            return False, blocks_to_move
        if (
            direction[1]
            and candidate in walls
            or (candidate[0] - 1, candidate[1]) in walls
        ):
            # case "##\n^." or "##\n.^" or "v.\n##" or ".v\n##"
            return False, blocks_to_move

        if direction[0] == 1 and candidate in food:
            # case ">[]"
            return try_move(
                (candidate[0] + 2, candidate[1]),
                direction,
                blocks_to_move | {candidate},
            )
        if direction[0] == -1 and (candidate[0] - 1, candidate[1]) in food:
            # case "[]<"
            return try_move(
                (candidate[0] - 2, candidate[1]),
                direction,
                blocks_to_move | {(candidate[0] - 1, candidate[1])},
            )
        if candidate in food:
            assert direction[1] and not direction[0]
            logger.debug("case []-^. or v.-[]")
            # case "[]\n^." or "v.\n[]"
            left, blocks_left = try_move(
                (candidate[0], candidate[1] + direction[1]),
                direction,
                blocks_to_move | {candidate},
            )
            right, blocks_right = try_move(
                (candidate[0] + 1, candidate[1] + direction[1]),
                direction,
                blocks_to_move | {candidate},
            )
            return left and right, blocks_left | blocks_right
        if (candidate[0] - 1, candidate[1]) in food:
            assert direction[1] and not direction[0]

            # case "[]\n.^" or ".v\n[]"
            logger.debug("case []-.^ or .v-[]")
            left, blocks_left = try_move(
                (candidate[0] - 1, candidate[1] + direction[1]),
                direction,
                blocks_to_move | {(candidate[0] - 1, candidate[1])},
            )
            right, blocks_right = try_move(
                (candidate[0], candidate[1] + direction[1]),
                direction,
                blocks_to_move | {(candidate[0] - 1, candidate[1])},
            )
            return left and right, blocks_left | blocks_right
        # else move to empty space
        return True, blocks_to_move

    for move in moves:
        # print_state(robot, food, walls)
        print(f"Move {move}:")
        dx, dy = move_map[move]
        new_robot = (robot[0] + dx, robot[1] + dy)
        can_move, blocks_to_move = try_move(new_robot, (dx, dy), set())
        if not can_move:
            continue
        if blocks_to_move:
            logger.debug("Blocks to move: %s in %s", blocks_to_move, (dx, dy))
            food_before = len(food)
            for block in blocks_to_move - {robot}:
                logger.debug("Removing moved food %s", block)
                food.remove(block)
            for block in blocks_to_move - {robot}:
                new_food = (block[0] + dx, block[1] + dy)
                logger.debug("Adding new food %s", new_food)
                food.add(new_food)

            assert len(food) == food_before
        robot = new_robot
    print_state_part2(robot, food, walls)
    part2 = sum(100 * y + x for x, y in food)
    logger.info("Part 2: %s", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
