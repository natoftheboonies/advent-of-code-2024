"""
Author: Nat with Darren's Template
Date: 2024-12-05

Solving https://adventofcode.com/2024/day/5
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 5

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


def check_page(page, rules):
    for rule in rules:
        left, right = rule
        if left in page and right in page and page.index(left) > page.index(right):
            return False
    return True


def fix_pages(pages, rules):
    for rule in rules:
        left, right = rule
        if left in pages and right in pages and pages.index(left) > pages.index(right):
            left_index = pages.index(left)
            right_index = pages.index(right)
            pages[left_index], pages[right_index] = (
                pages[right_index],
                pages[left_index],
            )
    return pages


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()

    # logger.debug(data)
    rules = []
    page_lists = []
    for line in data:
        if "|" in line:
            rule = list(map(int, line.split("|")))  # convert to list of ints
            rules.append(rule)
        elif "," in line:
            pages = list(map(int, line.split(",")))  # convert to list of ints
            page_lists.append(pages)

    # part 1
    result1 = 0
    incorrect = []
    for i, pages in enumerate(page_lists):
        if check_page(pages, rules):
            # logger.debug(f"{i}: {pages}")
            result1 += pages[len(pages) // 2]
        else:
            incorrect.append(pages)
    logger.info(f"Part 1: {result1}")

    # part 2
    fixed = []
    for pages in incorrect:
        while not check_page(pages, rules):
            pages = fix_pages(pages, rules)
        fixed.append(pages)
    result2 = sum(pages[len(pages) // 2] for pages in fixed)
    logger.info(f"Part 2: {result2}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
