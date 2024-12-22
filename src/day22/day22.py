"""
Author: Nat with Darren's Template
Date: 2024-12-22

Solving https://adventofcode.com/2024/day/22
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 22

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)

mix_and_prune = lambda a, b: a ^ b % 16777216


def next_number(number):
    number = mix_and_prune(number, number * 64)
    number = mix_and_prune(number, number // 32)
    number = mix_and_prune(number, number * 2048)
    return number


def main():
    puzzle = locations.input_file
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
        numbers = list(map(int, data))

    # logger.debug(numbers)

    history = list()
    price_chart = dict()

    for _ in range(2000):
        numbers = list(map(next_number, numbers))
        prices = list(map(lambda x: x % 10, numbers))  # get the last digit
        if history:
            price_changes = [p - h for p, h in zip(prices, history[-1])]
            history[-1] = price_changes

        if len(history) > 4:
            history.pop(0)
            for i, price in enumerate(prices):
                last_4 = tuple([h[i] for h in history])
                price_chart[last_4] = price_chart.get(last_4, 0) + price
        history.append(prices)

    logger.info("Part 1: %s", sum(numbers))
    # find max value in price_chart
    max_value = max(price_chart.values())
    logger.info("Max value in price_chart: %s", max_value)
    max_key = max(price_chart, key=price_chart.get)
    logger.info("Key for max value in price_chart: %s", max_key)

    # transform into [a,b,c,d]: sum


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
