"""
Author: Nat with Darren's Template
Date: 2024-12-14

Solving https://adventofcode.com/2024/day/14
"""

import logging
import time
import aoc_common.aoc_commons as ac
import re

YEAR = 2024
DAY = 14

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

robot_reg = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


boundary_x = 101
boundary_y = 103
move_robot = lambda x, y, vx, vy, c: (
    (x + vx * c) % boundary_x,
    (y + vy * c) % boundary_y,
)


def print_robots(robots):
    drone_show = [[" " for _ in range(boundary_x)] for _ in range(boundary_y)]
    for robot in robots:
        drone_show[robot[1]][robot[0]] = "R"
    return "\n".join("".join(drone_row) for drone_row in drone_show)


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    robots = []
    for line in data:
        rx, ry, vx, vy = map(int, robot_reg.match(line).groups())
        logger.debug(f"{rx}, {ry}, {vx}, {vy}")
        ex = (rx + vx * 100) % boundary_x
        ey = (ry + vy * 100) % boundary_y
        robots.append((ex, ey))
        logger.debug(f"{ex}, {ey}")

    # logger.debug(data)
    tl, tr, bl, br = 0, 0, 0, 0
    for robot in robots:
        if robot[0] < boundary_x // 2 and robot[1] < boundary_y // 2:
            tl += 1
        elif robot[0] > boundary_x // 2 and robot[1] < boundary_y // 2:
            tr += 1
        elif robot[0] < boundary_x // 2 and robot[1] > boundary_y // 2:
            bl += 1
        elif robot[0] > boundary_x // 2 and robot[1] > boundary_y // 2:
            br += 1
    safety_factor = tl * tr * bl * br
    logger.debug(f"tl: {tl}, tr: {tr}, bl: {bl}, br: {br}")
    logger.info(f"Part 1: {safety_factor}")

    robots = []
    for line in data:
        rx, ry, vx, vy = map(int, robot_reg.match(line).groups())
        robots.append([rx, ry, vx, vy])

    for t in range(1, 100000):
        for robot in robots:
            robot[0] = (robot[0] + robot[2]) % boundary_x
            robot[1] = (robot[1] + robot[3]) % boundary_y
        # look for cluster of robots
        drone_show = print_robots(robots)
        if "RRRRRRRR" in drone_show:
            print(drone_show)
            logger.info(f"Part 2: {t}")
            break


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
