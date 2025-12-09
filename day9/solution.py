def parse_coordinates(data):
    """Parse coordinate pairs from input."""
    coords = []
    for line in data.strip().split('\n'):
        if line.strip():
            x, y = map(int, line.split(','))
            coords.append((x, y))
    return coords


def calculate_rectangle_area(coord1, coord2):
    """Calculate the area of rectangle with opposite corners at coord1 and coord2."""
    x1, y1 = coord1
    x2, y2 = coord2
    # Inclusive counting: add 1 to each dimension
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def find_largest_rectangle(coords):
    """Find the largest rectangle area using any two coordinates as opposite corners."""
    max_area = 0
    best_coords = None

    # Try all pairs of coordinates
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            area = calculate_rectangle_area(coords[i], coords[j])
            if area > max_area:
                max_area = area
                best_coords = (coords[i], coords[j])

    return max_area, best_coords


def get_line_points(p1, p2):
    """Get all integer points on the line between p1 and p2."""
    x1, y1 = p1
    x2, y2 = p2
    points = set()

    # If same point, just return it
    if p1 == p2:
        return {p1}

    # If vertical line
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            points.add((x1, y))
    # If horizontal line
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            points.add((x, y1))

    return points


def point_in_polygon(point, polygon):
    """Check if a point is inside a polygon using ray casting algorithm."""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def is_point_on_edge(point, red_coords):
    """Check if a point is on the edge of the polygon."""
    for i in range(len(red_coords)):
        p1 = red_coords[i]
        p2 = red_coords[(i + 1) % len(red_coords)]

        # Check if point is on the line segment between p1 and p2
        x, y = point
        x1, y1 = p1
        x2, y2 = p2

        # Vertical line
        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return True
        # Horizontal line
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return True

    return False


def is_point_green(point, red_coords, red_tiles):
    """Check if a point is green (on edge or inside polygon, but not red)."""
    if point in red_tiles:
        return False

    # Check if on edge
    if is_point_on_edge(point, red_coords):
        return True

    # Check if inside polygon
    return point_in_polygon(point, red_coords)


def is_rectangle_valid(coord1, coord2, red_coords, red_tiles):
    """Check if rectangle contains only red or green tiles."""
    x1, y1 = coord1
    x2, y2 = coord2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # Check all points in the rectangle
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            point = (x, y)
            if point not in red_tiles and not is_point_green(point, red_coords, red_tiles):
                return False

    return True


def solve_part1(data):
    """Solve Part 1: Find largest rectangle area."""
    coords = parse_coordinates(data)
    max_area, best_coords = find_largest_rectangle(coords)
    return max_area


def solve_part2(data):
    """Solve Part 2: Find largest rectangle using only red and green tiles - OPTIMIZED."""
    coords = parse_coordinates(data)
    red_tiles = set(coords)
    n = len(coords)
    
    # Cache for point checks
    green_cache = {}
    
    def is_green_or_red(point):
        """Check if point is red or green (valid for rectangle)."""
        if point in red_tiles:
            return True
        if point in green_cache:
            return green_cache[point]
        
        # Check if on edge
        if is_point_on_edge(point, coords):
            green_cache[point] = True
            return True
        
        # Check if inside polygon
        result = point_in_polygon(point, coords)
        green_cache[point] = result
        return result

    def is_rectangle_valid_perimeter_only(p1, p2):
        """Check if rectangle perimeter contains only valid tiles."""
        x1, y1 = p1
        x2, y2 = p2
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        # Check horizontal sides
        for x in range(min_x, max_x + 1):
            if not is_green_or_red((x, min_y)): return False
            if not is_green_or_red((x, max_y)): return False
        
        # Check vertical sides
        for y in range(min_y + 1, max_y):
            if not is_green_or_red((min_x, y)): return False
            if not is_green_or_red((max_x, y)): return False
        
        return True

    max_area = 0
    
    # Build sorted list by area potential
    # print(f"Processing {n} coordinates, generating pairs...")
    coord_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            area = calculate_rectangle_area(coords[i], coords[j])
            coord_pairs.append((area, i, j))
    
    coord_pairs.sort(reverse=True)
    # print(f"Checking {len(coord_pairs)} pairs in descending area order...")
    
    checked = 0
    for area, i, j in coord_pairs:
        if area <= max_area:
            # print(f"Stopping early after {checked} checks (remaining pairs too small)")
            break
        
        if is_rectangle_valid_perimeter_only(coords[i], coords[j]):
            max_area = area
            # print(f"Found valid rectangle: area={area} at coords[{i}] and coords[{j}]")
        
        checked += 1
        # if checked % 50000 == 0:
            # print(f"Checked {checked}/{len(coord_pairs)} pairs, best area so far: {max_area}")
            
    # print(f"Final: checked {checked} pairs total")
    return max_area


if __name__ == "__main__":
    # Test with example
    example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    result1 = solve_part1(example)
    result2 = solve_part2(example)
    print(f"Example Part 1: {result1} (expected: 50)")
    print(f"Example Part 2: {result2} (expected: 24)")

    # Solve with actual input
    try:
        with open("input.txt", "r") as f:
            puzzle_input = f.read()
            if puzzle_input.strip():
                part1 = solve_part1(puzzle_input)
                part2 = solve_part2(puzzle_input)
                print(f"\nPart 1: {part1}")
                print(f"Part 2: {part2}")
            else:
                print("\nInput file is empty")
    except FileNotFoundError:
        print("\nNo input.txt file found")
