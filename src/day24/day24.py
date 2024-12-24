"""
Author: Nat with Darren's Template
Date: 2024-12-24

Solving https://adventofcode.com/2024/day/24
"""

import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2024
DAY = 24

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
    with open(puzzle, mode="rt") as f:  #
        known, computed = f.read().split("\n\n")
        known = map(lambda x: x.split(": "), known.splitlines())
        known = {k: int(v) for k, v in known}
        computed = map(lambda x: x.split(" -> "), computed.splitlines())
        all_z = set()
        rules = dict()
        for left, right in computed:
            left = tuple(left.split(" "))
            if right == "z01":
                logger.debug("right: %s", right)
            rules[right] = left
            if right.startswith("z"):
                all_z.add(right)

    # logger.debug(rules)

    while rules:
        for result, rule in rules.items():
            # if result == "z01":
            #     logger.debug("rule: %s", rule)
            now_known = set()
            left, op, right = rule
            if left in known and right in known:
                if op == "AND":
                    known[result] = known[left] & known[right]
                elif op == "OR":
                    known[result] = known[left] | known[right]
                elif op == "XOR":
                    known[result] = known[left] ^ known[right]
                now_known.add(result)
        for result in now_known:
            del rules[result]
        # if all(z in known for z in all_z):
        #     break
    known_result = ""
    for k in sorted(known, reverse=True):
        # print(f"{k}: {known[k]}")
        if k.startswith("z"):
            known_result += str(known[k])

    logger.debug("known_result: %s", known_result)
    # read known_result as binary
    known_result = "".join(map(str, known_result))
    logger.debug("known_result: %s", known_result)
    known_result = int(known_result, 2)
    logger.info("Part 1: %s", known_result)  # not 70368743653376


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
