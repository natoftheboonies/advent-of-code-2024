"""
Author: Nat with Darren's Template
Date: 2024-12-01

Solving https://adventofcode.com/2024/day/2
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 2

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def test_safe(nums):
    return (  # always increasing or always decreasing
        all(nums[i] > nums[i + 1] for i in range(len(nums) - 1))
        or all(nums[i] < nums[i + 1] for i in range(len(nums) - 1))
    ) and not any(  # no difference greater than 3
        abs(nums[i + 1] - nums[i]) > 3 for i in range(len(nums) - 1)
    )


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)

    unsafe = []
    # Part 1
    logger.info("Part 1")
    safe = 0
    for line in data:
        nums = [int(x) for x in line.split()]
        if test_safe(nums):
            safe += 1
        else:
            unsafe.append(nums)

    logger.info("#1: %s", safe)

    # part 2
    newly_safe = 0
    for nums in unsafe:
        for i in range(len(nums)):
            # test nums without index i
            if test_safe(nums[:i] + nums[i + 1 :]):
                newly_safe += 1
                break

    logger.info("#2: %s", safe + newly_safe)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
