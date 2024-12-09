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
        space = int(data[idx + 1]) if idx + 1 < len(data) else 0
        disk.append((file, space))
        idx += 2
    logger.debug(disk)
    idx = 0
    disk_seq = []
    while idx < len(disk):
        file, space = disk[idx]
        disk_seq += [idx] * file
        # logger.debug("prefix: %s %d", str(idx), file)
        while space > 0:
            end_idx = len(disk) - 1
            if end_idx == idx:
                break
            end_file, _ = disk[end_idx]
            move_file = min(space, end_file)
            file += move_file
            disk_seq += [end_idx] * move_file
            # logger.debug("suffix: %s %d", str(end_idx), move_file)
            end_file -= move_file
            space -= move_file

            if end_file == 0:
                disk.pop()
            else:
                disk[end_idx] = (end_file, 0)
            # logger.debug(f"disk (in): {disk}")
        disk[idx] = (file, space)

        idx += 1
    # logger.debug(disk_seq)
    checksum = 0
    for idx, c in enumerate(disk_seq):
        checksum += c * (idx)
    logger.info(f"Checksum: {checksum}")  # low 85635411453


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
