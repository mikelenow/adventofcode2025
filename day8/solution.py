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

    # For each frequency, find all pairs of antennas
    for frequency, positions in antennas.items():
        # Check all pairs of antennas with the same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]

                # Calculate the vector from pos1 to pos2
                dr = pos2[0] - pos1[0]
                dc = pos2[1] - pos1[1]

                # Antinode 1: on the opposite side of pos1 from pos2
                # This is where pos1 is twice as far from the antinode as pos2
                antinode1 = (pos1[0] - dr, pos1[1] - dc)

                # Antinode 2: on the opposite side of pos2 from pos1
                # This is where pos2 is twice as far from the antinode as pos1
                antinode2 = (pos2[0] + dr, pos2[1] + dc)

                # Check if antinodes are within bounds
                if 0 <= antinode1[0] < height and 0 <= antinode1[1] < width:
                    antinodes.add(antinode1)

                if 0 <= antinode2[0] < height and 0 <= antinode2[1] < width:
                    antinodes.add(antinode2)

    return antinodes

def main():
    grid = parse_input('input.txt')
    antinodes = find_antinodes(grid)
    result = len(antinodes)

    print(f"Number of unique antinode locations: {result}")

    with open('answer.txt', 'w') as f:
        f.write(str(result))

if __name__ == '__main__':
    main()
