import re

def parse_input(content):
    """Parses the input file into shapes and regions."""
    match = re.search(r'^\d+x\d+:', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find the start of the regions section in the input.")
    
    split_point = match.start()
    shapes_str = content[:split_point]
    regions_str = content[split_point:]

    # Parse shapes and their areas
    shapes = {}
    for shape_block in shapes_str.strip().split('\n\n'):
        if not shape_block.strip():
            continue
        lines = shape_block.strip().split('\n')
        shape_id = int(lines[0].split(':')[0])
        shape_drawing = lines[1:]
        area = sum(line.count('#') for line in shape_drawing)
        shapes[shape_id] = {'id': shape_id, 'area': area}

    # Parse regions and their requirements
    regions = []
    for line in regions_str.strip().split('\n'):
        if not line.strip():
            continue
        parts = [p for p in re.split(r'[x:\s]+', line.strip()) if p]
        width = int(parts[0])
        height = int(parts[1])
        counts = [int(c) for c in parts[2:]]
        regions.append({
            'width': width,
            'height': height,
            'counts': counts,
        })
    return shapes, regions

def main():
    """Main function to solve the puzzle."""
    try:
        with open("input.txt") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    shapes, regions = parse_input(content)
    
    solvable_by_area_count = 0
    total_regions = len(regions)
    print(f"Found {len(shapes)} shapes and {total_regions} regions.")

    for i, region in enumerate(regions):
        region_area = region['width'] * region['height']
        
        presents_area = 0
        for shape_id, count in enumerate(region['counts']):
            presents_area += count * shapes[shape_id]['area']
            
        print(f"Region {i+1} ({region['width']}x{region['height']}): Region Area = {region_area}, Presents Area = {presents_area}")

        if presents_area <= region_area:
            solvable_by_area_count += 1
            print("  -> PASSED area check.")
        else:
            print("  -> FAILED area check.")

    print(f"\nBased on the area check, {solvable_by_area_count} out of {total_regions} regions might be solvable.")
    print("\nThis problem is a complex packing puzzle. A simple area check is not enough to guarantee a solution.")
    print("However, if the total area of presents is larger than the region, it's definitely impossible.")
    print("The number of regions that pass the area check is the upper bound on the number of solvable regions.")
    print(f"Final Answer (based on area check): {solvable_by_area_count}")


if __name__ == "__main__":
    main()