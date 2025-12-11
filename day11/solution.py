import collections

def parse_input(filename="input.txt"):
    """
    Parses the input file into a graph (adjacency list).
    'aaa: bbb ccc' -> {'aaa': ['bbb', 'ccc']}
    """
    graph = collections.defaultdict(list)
    with open(filename) as f:
        for line in f:
            source, dests = line.strip().split(": ")
            graph[source].extend(dests.split())
    return graph

def part1(graph):
    """
    Solves Part 1: How many different paths lead from 'you' to 'out'?
    """
    memo = {}
    def count_paths(start, end):
        if start in memo:
            return memo[start]
        if start == end:
            return 1
        
        count = 0
        for neighbor in graph.get(start, []):
            count += count_paths(neighbor, end)
        
        memo[start] = count
        return count

    return count_paths('you', 'out')

def part2(graph):
    """
    Solves Part 2: How many paths from 'svr' to 'out' visit both 'dac' and 'fft'?
    """
    memo = {}
    checkpoints = frozenset(['dac', 'fft'])

    def solve(node, checkpoints_to_visit):
        state = (node, checkpoints_to_visit)
        if state in memo:
            return memo[state]

        if node == 'out':
            # A path is valid only if it ends at 'out' AND all checkpoints have been visited.
            return 1 if not checkpoints_to_visit else 0

        total_paths = 0
        for neighbor in graph.get(node, []):
            new_checkpoints = checkpoints_to_visit
            if neighbor in new_checkpoints:
                new_checkpoints = new_checkpoints - {neighbor}
            total_paths += solve(neighbor, new_checkpoints)
        
        memo[state] = total_paths
        return total_paths

    return solve('svr', checkpoints)


if __name__ == "__main__":
    graph = parse_input()
    
    # --- Part 1 ---
    result_part1 = part1(graph)
    print(f"Part 1: {result_part1}")

    # --- Part 2 ---
    result_part2 = part2(graph)
    print(f"Part 2: {result_part2}")