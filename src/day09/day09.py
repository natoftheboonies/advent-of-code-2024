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


def build_disk(data):
    idx = 0
    disk = []
    while idx < len(data):
        file_id = idx // 2
        blocks = int(data[idx])
        free = int(data[idx + 1]) if idx + 1 < len(data) else 0
        disk.append((file_id, blocks, free))
        if blocks == 0:
            logger.warning("zero file size at %d", idx)
            assert False
        idx += 2
    return disk


def calc_checksum(disk):
    checksum = 0
    block_id = 0
    for file_id, blocks, free in disk:
        checksum += file_id * (block_id * blocks + blocks * (blocks - 1) // 2)
        block_id += blocks + free
    return checksum


def part1(disk):
    idx = 0
    while idx < len(disk):
        # fill the free space
        file_id, blocks, free = disk[idx]
        if free > 0:
            end_idx = len(disk) - 1
            if end_idx == idx:
                break
            end_id, end_blocks, _ = disk[end_idx]
            # how much of end_file can we take?
            move_blocks = min(free, end_blocks)
            if move_blocks == end_blocks:
                disk.pop(end_idx)
            else:
                disk[end_idx] = (end_id, end_blocks - move_blocks, 0)
            disk.insert(idx + 1, (end_id, move_blocks, free - move_blocks))
            disk[idx] = (file_id, blocks, 0)
        idx += 1

    return calc_checksum(disk)


def part2(disk):
    idx = len(disk) - 1
    checked = set()
    while idx > 0:
        # can we move this file?
        move_id, move_blocks, move_free = disk[idx]
        assert move_blocks > 0
        if move_id in checked:
            # logger.debug("already checked %d", move_key)
            idx -= 1
            continue

        # logger.debug(f"can we move key: {move_key}")
        checked.add(move_id)
        for i in range(idx):
            dest_id, dest_blocks, dest_free = disk[i]
            if dest_free >= move_blocks:
                # yes, it fits
                disk.pop(idx)

                # extend the free space before the removed file
                before_id, before_blocks, before_free = disk[idx - 1]
                disk[idx - 1] = (
                    before_id,
                    before_blocks,
                    before_free + move_blocks + move_free,
                )

                # consume the destination free space, as we append it to the moved file
                disk[i] = (dest_id, dest_blocks, 0)
                # insert the moved file after with any remaining free space
                disk.insert(i + 1, (move_id, move_blocks, dest_free - move_blocks))
                # skip decrementing idx, as we inserted an element
                break
        else:  # no move found
            idx -= 1

    return calc_checksum(disk)


def run_sample():
    puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().strip()

    disk = build_disk(data)
    part1_checksum = part1(disk)
    logger.info(f"Checksum: {part1_checksum}")
    assert part1_checksum == 1928

    disk = build_disk(data)
    part2_checksum = part2(disk)
    logger.info(f"Checksum: {part2_checksum}")
    assert part2_checksum == 2858


def build_disk_again(data):
    idx = 0
    files = []
    free_spaces = []
    block_id = 0
    while idx < len(data):
        file_id = idx // 2
        blocks = int(data[idx])
        free = int(data[idx + 1]) if idx + 1 < len(data) else 0
        files.append([block_id, blocks, file_id])
        block_id += blocks
        if free > 0:
            free_spaces.append([block_id, free])
            block_id += free
        idx += 2
    return files, free_spaces


def main():
    # run_sample()

    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().strip()

    disk = build_disk(data)
    part1_checksum = part1(disk)
    logger.info(f"Part 1: {part1_checksum}")
    # assert part1_checksum == 6359213660505

    # disk = build_disk(data)
    # part2_checksum = part2(disk)
    # logger.info(f"Checksum: {part2_checksum}")  # 6381528943428 < answer < 6381625147860
    # assert part2_checksum == 6381624803796
    files, free_spaces = build_disk_again(data)

    # files are (index, size, file_id)

    for file in reversed(files):
        for free_space in free_spaces:
            if free_space[0] >= file[0]:
                break  # no moving files backwards
            if file[1] <= free_space[1]:
                # logger.debug(f"moving {file} to {free_space}")
                file[0] = free_space[0]
                # reduce and shift free space
                free_space[1] = free_space[1] - file[1]
                free_space[0] = free_space[0] + file[1]

    checksum_again = 0
    for i, n, id in files:
        checksum_again += id * (i * n + n * (n - 1) // 2)
    logger.info(f"Part 2: {checksum_again}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
