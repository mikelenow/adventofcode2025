def parse_input(filename):
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]

def find_start(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return (row, col)
    return None

def simulate_beams(grid):
    start_pos = find_start(grid)
    if not start_pos:
        return 0

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Track active beam columns at each row
    # Beams always move downward, one row at a time
    # When a beam encounters a splitter, it stops and creates beams to the left and right

    current_row = start_pos[0]
    active_beams = {start_pos[1]}  # Set of column positions with active beams
    split_count = 0

    # Process row by row
    while current_row < height - 1 and active_beams:
        current_row += 1
        next_beams = set()

        # For each active beam, check what it encounters in the next row
        for col in active_beams:
            if 0 <= col < width:
                char = grid[current_row][col]

                if char == '.' or char == 'S':
                    # Beam continues downward
                    next_beams.add(col)
                elif char == '^':
                    # Splitter! Beam stops, create two new beams
                    split_count += 1
                    # Add beams to the left and right
                    if col - 1 >= 0:
                        next_beams.add(col - 1)
                    if col + 1 < width:
                        next_beams.add(col + 1)

        active_beams = next_beams

    return split_count

def main():
    grid = parse_input('input.txt')
    result = simulate_beams(grid)
    print(f"The beam will be split {result} times")

    with open('answer.txt', 'w') as f:
        f.write(str(result))

if __name__ == '__main__':
    main()
