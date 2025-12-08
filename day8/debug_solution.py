def parse_input(filename):
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]

def find_antennas(grid):
    """Find all antennas and group them by frequency."""
    antennas = {}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            char = grid[row][col]
            if char != '.':
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((row, col))
    return antennas

def find_antinodes(grid):
    """Find all antinode locations within the grid bounds."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    antennas = find_antennas(grid)
    antinodes = set()

    print(f"Grid size: {height}x{width}")
    print(f"Antennas found: {antennas}")
    print()

    # For each frequency, find all pairs of antennas
    for frequency, positions in antennas.items():
        print(f"\nProcessing frequency '{frequency}' with {len(positions)} antennas:")
        print(f"Positions: {positions}")

        # Check all pairs of antennas with the same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]

                print(f"\n  Pair: {pos1} and {pos2}")

                # Calculate the vector from pos1 to pos2
                dr = pos2[0] - pos1[0]
                dc = pos2[1] - pos1[1]
                print(f"  Vector: dr={dr}, dc={dc}")

                # Antinode 1: on the opposite side of pos1 from pos2
                antinode1 = (pos1[0] - dr, pos1[1] - dc)
                print(f"  Antinode1: {antinode1}", end="")

                # Antinode 2: on the opposite side of pos2 from pos1
                antinode2 = (pos2[0] + dr, pos2[1] + dc)
                print(f", Antinode2: {antinode2}")

                # Check if antinodes are within bounds
                if 0 <= antinode1[0] < height and 0 <= antinode1[1] < width:
                    antinodes.add(antinode1)
                    print(f"    -> Added antinode1 {antinode1}")
                else:
                    print(f"    -> antinode1 {antinode1} out of bounds")

                if 0 <= antinode2[0] < height and 0 <= antinode2[1] < width:
                    antinodes.add(antinode2)
                    print(f"    -> Added antinode2 {antinode2}")
                else:
                    print(f"    -> antinode2 {antinode2} out of bounds")

    return antinodes

def visualize_antinodes(grid, antinodes):
    """Show the grid with antinodes marked."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    print("\n\nGrid with antinodes (#):")
    for row in range(height):
        line = ""
        for col in range(width):
            if (row, col) in antinodes:
                if grid[row][col] != '.':
                    line += grid[row][col]  # Show antenna if there
                else:
                    line += '#'
            else:
                line += grid[row][col]
        print(line)

def main():
    grid = parse_input('input.txt')
    antinodes = find_antinodes(grid)
    visualize_antinodes(grid, antinodes)

    result = len(antinodes)
    print(f"\n\nTotal unique antinode locations: {result}")
    print(f"Expected: 14")

if __name__ == '__main__':
    main()
