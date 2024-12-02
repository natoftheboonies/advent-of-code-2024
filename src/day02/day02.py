"""
Author: Nat with Darren's Template
Date: 2024-12-01

Solving https://adventofcode.com/2024/day/2

Part 1:

Part 2:

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
    decrease = None

    ok = False
    for i, n in enumerate(nums):
        if i == 0:
            continue
        if decrease == True and n >= nums[i - 1]:
            break
        if decrease == False and n <= nums[i - 1]:
            break
        if decrease == None and n == nums[i - 1]:
            logger.debug("same failed part 1: %s", nums)
            break
        if decrease == None and n < nums[i - 1]:
            decrease = True
            logger.debug("detected decrease: %s", nums)
        if decrease == None and n > nums[i - 1]:
            decrease = False
            logger.debug("detected increase: %s", nums)
    else:
        ok = True
        logger.debug("passed part 1: %s", nums)
    if not ok:
        return False

    for i, n in enumerate(nums):
        if i == 0:
            continue
        if abs(n - nums[i - 1]) > 3:
            logger.debug("failed part 2: %s", n)
            break

    else:
        logger.debug("passed part 2: %s", nums)
        return True
    return False


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)

    unsafe = []
    # Part 1
    logger.info("Part 1")
    result = 0
    for line in data:
        nums = [int(x) for x in line.split()]
        if test_safe(nums):
            result += 1
        else:
            unsafe.append(nums)

        # if len(nums) != len(set(nums)):
        #     continue

    # not 298, 485, 408
    logger.info("#1: %s", result)

    # part 2
    newly_safe = 0
    for nums in unsafe:
        for i in range(len(nums)):
            # test nums without index i
            if test_safe(nums[:i] + nums[i + 1 :]):
                newly_safe += 1
                break

    logger.info("#2: %s", result + newly_safe)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
