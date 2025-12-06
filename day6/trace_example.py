# Let me trace through the example step by step to understand the algorithm

example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

lines = example.strip().split('\n')

# Make sure all lines are same length
max_len = max(len(line) for line in lines)
lines = [line.ljust(max_len) for line in lines]

print("Column-by-column breakdown:")
print("=" * 60)

for col in range(max_len):
    chars = [line[col] for line in lines]
    print(f"Column {col:2d}: {chars} → ", end="")

    # Check what's in this column
    digits = [c for c in chars if c.isdigit()]
    operator = [c for c in chars if c in ['+', '*']]

    if digits:
        number = ''.join(digits)
        print(f"Number: {number}", end="")
    if operator:
        print(f" Operator: {operator[0]}", end="")
    if not digits and not operator:
        print("Empty/separator", end="")
    print()

print("\n" + "=" * 60)
print("Now let's trace the Rust algorithm:")
print("=" * 60)

current_problem_numbers = []
grand_total = 0

# Process columns RIGHT to LEFT
for col in range(max_len - 1, -1, -1):
    number_string = []
    operator = None

    # Read column top to bottom
    for line in lines:
        char = line[col]
        if char.isdigit():
            number_string.append(char)
        elif char in ['+', '*']:
            operator = char

    print(f"\nColumn {col}: ", end="")

    # If we found an operator
    if operator:
        # Add current number (if any) to problem
        if number_string:
            number = int(''.join(number_string))
            current_problem_numbers.append(number)
            print(f"digits='{' '.join(number_string)}' → {number}, ", end="")

        print(f"operator={operator}")
        print(f"  → Problem ends! Numbers accumulated: {current_problem_numbers}")

        # Calculate result
        if operator == '+':
            result = sum(current_problem_numbers)
            print(f"  → {' + '.join(map(str, current_problem_numbers))} = {result}")
        else:
            result = 1
            for n in current_problem_numbers:
                result *= n
            print(f"  → {' * '.join(map(str, current_problem_numbers))} = {result}")

        grand_total += result
        print(f"  → Grand total so far: {grand_total}")
        current_problem_numbers = []

    # If no operator but we have digits
    elif number_string:
        number = int(''.join(number_string))
        current_problem_numbers.append(number)
        print(f"digits='{' '.join(number_string)}' → {number}, accumulate")
        print(f"  → Numbers so far: {current_problem_numbers}")

    # If nothing
    else:
        print("empty (skip)")

print(f"\n{'=' * 60}")
print(f"Final grand total: {grand_total}")
print(f"Expected: 3263827")
