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
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def part1(plots):
    part1 = 0
    for c, plot in plots:
        area = len(plot)
        perimeter = 0
        for x, y in plot:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in plot:
                    perimeter += 1
        part1 += area * perimeter
    return part1


def count_continuous_sequences(lst):
    if not lst:
        return 0

    lst.sort()
    sequences = []
    current_sequence = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] == lst[i - 1] + 1:
            current_sequence.append(lst[i])
        else:
            sequences.append(current_sequence)
            current_sequence = [lst[i]]

    sequences.append(current_sequence)
    return sequences


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)

    plots = []

    for ey, line in enumerate(data):
        for ex, c in enumerate(line):
            for _, plot in plots:
                if (ex, ey) in plot:
                    break
            else:
                # new plot to explore!
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

    logger.info("Part 1: %s", part1(plots))

    total_price = 0
    for c, plot in plots:
        # calc sides
        sides = {(0, 1): set(), (1, 0): set(), (0, -1): set(), (-1, 0): set()}
        for x, y in plot:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in plot:
                    sides[(dx, dy)].add((nx, ny))
        # logger.debug(f"Plot {c} sides: {sides}")
        side_count = 0
        for side, points in sides.items():
            count = 0
            if side[0] == 0:
                unique_y = set()
                for x, y in points:
                    unique_y.add(y)
                for y in unique_y:
                    filtered_points = [p[0] for p in points if p[1] == y]
                    filtered_points.sort()
                    sequences = count_continuous_sequences(filtered_points)
                    count += len(sequences)
            else:
                unique_x = set()
                for x, y in points:
                    unique_x.add(x)
                for x in unique_x:
                    filtered_points = [p[1] for p in points if p[0] == x]
                    filtered_points.sort()
                    sequences = count_continuous_sequences(filtered_points)
                    count += len(sequences)
            side_count += count

        area = len(plot)
        price = area * side_count
        logger.debug(
            f"A region of {c} plants with price {area} * {side_count} = {price}"
        )
        total_price += price
    logger.info("Part 2: %s", total_price)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
