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
                return best_cost, shortest
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

    maze = base_maze.copy()
    baseline_cost, shortest = run_maze()

    threshold = 100

    part1 = 0
    for x, y in shortest.keys():
        for nx, ny in (x + 2, y), (x + 1, y + 1), (x, y + 2), (x, y - 1):
            if nx < 0 or nx >= bound_x or ny < 0 or ny >= bound_y:
                continue
            if (nx, ny) in maze:
                continue
            if abs(shortest[(x, y)] - shortest[(nx, ny)]) >= threshold + 2:
                part1 += 1

    logger.info("Part 1: %s", part1)

    part2 = 0
    path_seq = list(shortest.keys())
    for i in range(len(path_seq)):
        bx, by = path_seq[i]
        for j in range(i + 1, len(path_seq)):
            ex, ey = path_seq[j]
            dist = abs(bx - ex) + abs(by - ey)
            if (
                dist <= 20
                and abs(shortest[(bx, by)] - shortest[(ex, ey)]) >= threshold + dist
            ):
                part2 += 1

    logger.info("Part 2: %s", part2)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
