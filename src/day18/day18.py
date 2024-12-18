"""
Author: Nat with Darren's Template
Date: 2024-12-18

Solving https://adventofcode.com/2024/day/18
"""

import logging
import time
import aoc_common.aoc_commons as ac
import heapq

YEAR = 2024
DAY = 18

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
        bytes = list(tuple(map(int, byte.split(","))) for byte in data)

    # logger.debug(bytes)
    initial_bytes = 1024
    bound = 71

    maze = bytes[:initial_bytes]
    start = (0, 0)

    end = (bound - 1, bound - 1)

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
                    or new_pos[0] >= bound
                    or new_pos[1] < 0
                    or new_pos[1] >= bound
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

    cost, path = run_maze()
    logger.info("Part 1: %s", cost)

    # binary search from initial_bytes to len(bytes)
    left, right = initial_bytes, len(bytes) - 1
    while left <= right:
        mid = (left + right) // 2
        maze = bytes[:mid]
        cost, path = run_maze()
        if cost == -1:
            right = mid - 1
        else:
            left = mid + 1
    next_byte = bytes[right]

    logger.info("Part 2: %s", ",".join(map(str, next_byte)))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
