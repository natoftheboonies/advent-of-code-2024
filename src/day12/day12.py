"""
Author: Nat with Darren's Template
Date: 2024-12-12

Solving https://adventofcode.com/2024/day/12
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 12

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

    plots = []

    for ey, line in enumerate(data):
        for ex, c in enumerate(line):
            # logger.debug(f"({ex},{ey}): {c}")
            for _, plot in plots:
                if (ex, ey) in plot:
                    break
            else:
                # new plot to explore!
                logger.debug(f"New plot {c} at ({ex},{ey})")
                queue = [(ex, ey)]
                plot = set()
                while queue:
                    x, y = queue.pop()
                    if (x, y) in plot:
                        continue
                    plot.add((x, y))
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if nx < 0 or nx >= len(line) or ny < 0 or ny >= len(data):
                            continue
                        if data[ny][nx] == c:
                            queue.append((nx, ny))
                plots.append((c, plot))

    logger.debug(plots)

    part1 = 0
    for c, plot in plots:
        area = len(plot)
        perimeter = 0
        for x, y in plot:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in plot:
                    perimeter += 1
        logger.debug(f"Plot {c} with area {area} and perimeter {perimeter}")
        part1 += area * perimeter

    logger.info("Part 1: %s", part1)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
