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
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
        numbers = list(map(int, data))

    # logger.debug(numbers)

    history = list()
    # transform into [a,b,c,d]: sum
    price_chart = dict()
    # only first time a sequence is seen
    seen_sequences = [set() for _ in numbers]

    sample_best = (-2, 1, -1, 3)

    for _ in range(2000):
        numbers = list(map(next_number, numbers))
        prices = list(map(lambda x: x % 10, numbers))  # get the last digit
        if len(history) > 0:
            price_changes = [p - h for p, h in zip(prices, history[-1])]
            history[-1] = price_changes

        if len(history) == 4:
            for i, price in enumerate(prices):
                last_4 = tuple([h[i] for h in history])
                if last_4 == sample_best:
                    logger.debug(f"{sample_best}: {price} for seq {i}")
                if last_4 in seen_sequences[i]:
                    continue
                seen_sequences[i].add(last_4)
                price_chart[last_4] = price_chart.get(last_4, 0) + price
            history.pop(0)
        history.append(prices)

    logger.info("Part 1: %s", sum(numbers))
    # find max value in price_chart
    max_value = max(price_chart.values())
    logger.info("Part 2: %s", max_value)
    max_key = max(price_chart, key=price_chart.get)
    logger.debug("for key: %s", max_key)
    logger.debug(price_chart[sample_best])


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
