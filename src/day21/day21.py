"""
Author: Nat with Darren's Template
Date: 2024-12-21

Solving https://adventofcode.com/2024/day/21
"""

import logging
import time
import aoc_common.aoc_commons as ac
from functools import cache

YEAR = 2024
DAY = 21

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


# credit to https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m35qlna/
def create_keypad(keys):
    def press(start, end):
        start_idx = keys.index(start)
        end_idx = keys.index(end)
        gap_idx = keys.index("_")

        y_diff = (end_idx // 3) - (start_idx // 3)
        x_diff = (end_idx % 3) - (start_idx % 3)

        x_moves = (">" if x_diff > 0 else "<") * abs(x_diff)
        y_moves = ("v" if y_diff > 0 else "^") * abs(y_diff)

        # moving y would cross gap
        if end_idx // 3 == gap_idx // 3 and start_idx % 3 == gap_idx % 3:
            return x_moves + y_moves
        # moving x would cross gap
        elif start_idx // 3 == gap_idx // 3 and end_idx % 3 == gap_idx % 3:
            return y_moves + x_moves
        else:
            # move order: <, v, ^, >
            if ">" in x_moves:
                return y_moves + x_moves
            else:
                return x_moves + y_moves

    return press


numeric = """
789
456
123
_0A
""".strip().replace(
    "\n", ""
)
keypad_numeric = create_keypad(numeric)

directional = """
_^A
<v>
""".strip().replace(
    "\n", ""
)
keypad_directional = create_keypad(directional)


def count_keypad_steps(code, keypad_chain):

    @cache
    def count_keypress(current, target, depth):
        sequence = keypad_chain[depth](current, target) + "A"
        if depth == len(keypad_chain) - 1:
            return len(sequence)
        else:
            length = 0
            current = "A"
            for target in sequence:
                length += count_keypress(current, target, depth + 1)
                current = target
            return length

    length = 0
    current = "A"
    for target in code:
        length += count_keypress(current, target, 0)
        current = target
    return length


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
        assert len(data) == 5

    keypad_chain = [keypad_numeric] + [keypad_directional] * 2
    part2_keypad_chain = [keypad_numeric] + [keypad_directional] * 25

    part1 = 0
    part2 = 0
    for code in data:
        sequence_length = count_keypad_steps(code, keypad_chain)
        sequence_length_part2 = count_keypad_steps(code, part2_keypad_chain)
        multiplier = int("".join(n for n in code if n.isdigit()))
        result = sequence_length * multiplier
        logger.debug(f"{code}: {sequence_length} * {multiplier} = {result}")
        part1 += result
        part2 += sequence_length_part2 * multiplier

    logger.info(f"Part 1: {part1}")
    logger.info(f"Part 2: {part2}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
