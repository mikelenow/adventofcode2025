def parse_input(filename):
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]

def find_start(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return (row, col)
    return None

def count_timelines(grid):
    start_pos = find_start(grid)
    if not start_pos:
        return 0

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Track number of timelines at each column position
    # timelines[col] = number of timelines with particle at this column
    current_row = start_pos[0]
    timelines = {start_pos[1]: 1}  # Start with 1 timeline at starting column

    # Process row by row
    while current_row < height - 1 and timelines:
        current_row += 1
        next_timelines = {}

        # For each column with timelines
        for col, count in timelines.items():
            if 0 <= col < width:
                char = grid[current_row][col]

                if char == '.' or char == 'S':
                    # Particle continues downward in all timelines
                    next_timelines[col] = next_timelines.get(col, 0) + count
                elif char == '^':
                    # Splitter: each timeline splits into 2
                    # One goes left, one goes right
                    left_col = col - 1
                    right_col = col + 1

                    if left_col >= 0:
                        next_timelines[left_col] = next_timelines.get(left_col, 0) + count
                    if right_col < width:
                        next_timelines[right_col] = next_timelines.get(right_col, 0) + count

        timelines = next_timelines

    # Sum up all timelines at the end
    total_timelines = sum(timelines.values())
    return total_timelines

def main():
    grid = parse_input('input.txt')
    result = count_timelines(grid)
    print(f"Total number of timelines: {result}")

    with open('answer_part2.txt', 'w') as f:
        f.write(str(result))

if __name__ == '__main__':
    main()
