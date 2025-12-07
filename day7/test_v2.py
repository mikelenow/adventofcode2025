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

    print(f"Starting at row {current_row}, column {start_pos[1]}")
    print(f"Grid size: {height}x{width}\n")

    # Process row by row
    while current_row < height - 1 and active_beams:
        current_row += 1
        next_beams = set()

        print(f"Row {current_row}: {len(active_beams)} active beams at columns {sorted(active_beams)}")

        # For each active beam, check what it encounters in the next row
        for col in sorted(active_beams):
            if 0 <= col < width:
                char = grid[current_row][col]
                print(f"  Col {col}: '{char}'", end="")

                if char == '.' or char == 'S':
                    # Beam continues downward
                    next_beams.add(col)
                    print(" -> continues")
                elif char == '^':
                    # Splitter! Beam stops, create two new beams
                    split_count += 1
                    print(f" -> SPLIT #{split_count}", end="")
                    # Add beams to the left and right
                    new_cols = []
                    if col - 1 >= 0:
                        next_beams.add(col - 1)
                        new_cols.append(col - 1)
                    if col + 1 < width:
                        next_beams.add(col + 1)
                        new_cols.append(col + 1)
                    print(f" creating beams at {new_cols}")

        active_beams = next_beams
        print()

    print(f"\nTotal splits: {split_count}")
    return split_count

def main():
    grid = parse_input('test_input.txt')
    result = simulate_beams(grid)
    print(f"\nFinal result: The beam will be split {result} times")

if __name__ == '__main__':
    main()
