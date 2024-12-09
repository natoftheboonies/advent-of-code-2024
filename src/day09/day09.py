"""
Author: Nat with Darren's Template
Date: 2024-12-09

Solving https://adventofcode.com/2024/day/9
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 9

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def part1(disk):
    idx = 0

    while idx < len(disk):
        key, file, free = disk[idx]
        # logger.debug("prefix: %s %d", str(idx), file)
        if free > 0:
            end_idx = len(disk) - 1
            if end_idx == idx:
                break
            end_key, end_file, _ = disk[end_idx]
            # how much of end_file can we take?
            move_file = min(free, end_file)
            if move_file == end_file:
                disk.pop(end_idx)
            else:
                disk[end_idx] = (end_key, end_file - move_file, 0)
            disk = (
                disk[: idx + 1]
                + [(end_key, move_file, free - move_file)]
                + disk[idx + 1 :]
            )
            free -= move_file
            disk[idx] = (key, file, 0)
            # logger.debug("suffix: %s %d", str(end_idx), move_file)
            # logger.debug(f"disk (in): {disk}")
        idx += 1
    checksum = 0
    disk_seq = []
    for idx, c, free in disk:
        disk_seq.extend([idx] * c)
        disk_seq.extend(["."] * free)
    # logger.info(f"disk_seq: {disk_seq}")

    for idx, c in enumerate(disk_seq):
        checksum += idx * c
    return checksum


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().strip()

    # logger.debug(data)
    idx = 0
    disk = []
    while idx < len(data):
        file = int(data[idx])
        free = int(data[idx + 1]) if idx + 1 < len(data) else 0
        disk.append((idx // 2, file, free))
        idx += 2
    # logger.debug(disk)

    logger.info(f"Checksum: {part1(disk)}")  # low 85635411453


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
