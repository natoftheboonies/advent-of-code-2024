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
        rules = dict()
        for left, right in computed:
            left = tuple(left.split(" "))
            rules[right] = left

    part2 = rules.copy()

    while rules:
        for result, rule in rules.items():
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
    known_result = ""
    for k in sorted(known, reverse=True):
        # print(f"{k}: {known[k]}")
        if k.startswith("z"):
            known_result += str(known[k])

    logger.debug("known_result: %s", known_result)
    # read known_result as binary
    known_result = int(known_result, 2)
    logger.info("Part 1: %s", known_result)  # not 70368743653376

    # Part 2
    # credit to https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3llouk/
    # find rules yielding z* without XOR
    output_rules = {k for k, v in part2.items() if v[1] != "XOR" and k.startswith("z")}
    output_rules.remove("z45")  # last carry bit ok
    logger.debug("output_rules: %s", output_rules)
    # find XOR rules without x* or y* inputs
    input_rules = {
        k
        for k, v in part2.items()
        if not k.startswith("z")
        and v[1] == "XOR"
        and not any(x.startswith("x") or x.startswith("y") for x in v)
    }
    logger.debug("input_rules: %s", input_rules)
    # find OR inputs not AND outputs
    and_outputs = {
        k
        for k, v in part2.items()
        if v[1] == "AND" and not ("x00" in v and "y00" in v)  # first bit
    }
    or_inputs = {v[0] for k, v in part2.items() if v[1] == "OR"} | {
        v[2] for k, v in part2.items() if v[1] == "OR"
    }
    # symmetric difference
    net_inputs = or_inputs ^ and_outputs
    logger.debug("and ^ or: %s", net_inputs)
    combined = input_rules | output_rules | net_inputs
    logger.info("Part 2: %s", ",".join(sorted(combined)))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
