"""
Author: Nat with Darren's Template
Date: 2024-12-22

Solving https://adventofcode.com/2024/day/23
"""

import logging
import time
import aoc_common.aoc_commons as ac
from collections import defaultdict
from itertools import combinations

YEAR = 2024
DAY = 23

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)


# thx chatgpt: TIL cliques and Bron–Kerbosch algorithm.
def bron_kerbosch(R: set, P: set, X: set, graph: dict, cliques: list):
    """Bron-Kerbosch algorithm to find all maximal cliques in a graph."""
    if not P and not X:  # Base case: no more candidates to add
        cliques.append(R)  # Found a maximal clique
        return
    for v in list(P):  # Iterate over a copy of P to allow modifications
        bron_kerbosch(
            R.union({v}),  # Add vertex to the current clique
            P.intersection(graph[v]),  # Neighbors of v
            X.intersection(graph[v]),  # Exclude neighbors of v
            graph,
            cliques,
        )
        P.remove(v)  # Remove v from P
        X.add(v)  # Add v to X to exclude it in future branches


def find_maximal_cliques(graph):
    """Find all maximal cliques in the graph."""
    cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, cliques)
    return cliques


def find_maximum_clique(graph):
    """Find the largest clique in the graph."""
    cliques = find_maximal_cliques(graph)
    return max(cliques, key=len)  # Return the largest clique


def main():
    puzzle = locations.input_file
    # puzzle = locations.sample_input_file
    with open(puzzle, mode="rt") as f:
        data = f.read().splitlines()
    connections = [line.split("-") for line in data]
    graph = defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)

    t3_cliques = set()
    for key, value in graph.items():
        if not key.startswith("t"):
            continue
        for connection in value:
            joint_friends = graph[connection].intersection(value)
            for friend in joint_friends:
                t3_cliques.add(tuple(sorted([key, connection, friend])))
    logger.info("Part 1: %s", len(t3_cliques))

    max_clique = find_maximum_clique(graph)
    password = ",".join(sorted(max_clique))
    logger.info("Part 2: %s", password)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
