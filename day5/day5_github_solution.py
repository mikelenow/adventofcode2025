#!/usr/bin/env python3

def part2(data):
    blank = data.index("")
    ranges = sorted([list(map(int, i.split("-"))) for i in data[:blank]])

    merged = [ranges[0]]
    for x2, y2 in ranges[1:]:
        x1, y1 = merged[-1]
        if x2 > y1:
            merged.append([x2, y2])
        else:
            merged[-1][1] = max(y1, y2)

    total = sum(y - x + 1 for x, y in merged)
    return total

# Read input
with open('day5_input.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]

result = part2(data)
print(f"Part 2 Answer: {result}")
