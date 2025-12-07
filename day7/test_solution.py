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

    # Track beams: each beam is (row, col, direction)
    # direction: 'down', 'left', 'right'
    beams = [(start_pos[0], start_pos[1], 'down')]
    split_count = 0

    # Track visited states to avoid infinite loops
    visited = set()

    print(f"Starting at {start_pos}")
    print(f"Grid size: {height}x{width}")

    step = 0
    while beams:
        step += 1
        print(f"\nStep {step}: {len(beams)} beams")
        new_beams = []

        for beam_idx, (row, col, direction) in enumerate(beams):
            # Create state for this beam
            state = (row, col, direction)
            if state in visited:
                print(f"  Beam {beam_idx} at ({row}, {col}) going {direction} already visited")
                continue
            visited.add(state)

            # Move beam one step
            if direction == 'down':
                next_row = row + 1
                next_col = col
            elif direction == 'left':
                next_row = row
                next_col = col - 1
            elif direction == 'right':
                next_row = row
                next_col = col + 1
            else:
                continue

            # Check if beam is out of bounds
            if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
                print(f"  Beam {beam_idx} at ({row}, {col}) going {direction} exits bounds at ({next_row}, {next_col})")
                continue

            # Check what's at the next position
            next_char = grid[next_row][next_col]

            print(f"  Beam {beam_idx} at ({row}, {col}) going {direction} -> ({next_row}, {next_col}) '{next_char}'")

            if next_char == '.':
                # Continue in same direction
                new_beams.append((next_row, next_col, direction))
            elif next_char == '^':
                # Splitter: beam stops, create two new beams going left and right
                split_count += 1
                print(f"    SPLIT #{split_count} at ({next_row}, {next_col})")
                new_beams.append((next_row, next_col, 'left'))
                new_beams.append((next_row, next_col, 'right'))
            elif next_char == 'S':
                # Shouldn't happen, but treat as empty
                new_beams.append((next_row, next_col, direction))

        beams = new_beams

        if step > 100:
            print("Too many steps, breaking")
            break

    return split_count

def main():
    grid = parse_input('test_input.txt')
    result = simulate_beams(grid)
    print(f"\nFinal result: The beam will be split {result} times")

if __name__ == '__main__':
    main()
