def solve_worksheet_part2(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Ensure all lines have the same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    grand_total = 0
    current_problem_numbers = []

    # Process columns from RIGHT to LEFT
    for col in range(max_len - 1, -1, -1):
        # Read this column vertically (top to bottom)
        number_digits = []
        operator = None

        for line in lines:
            char = line[col]
            if char.isdigit():
                number_digits.append(char)
            elif char in ['+', '*']:
                operator = char

        # If we found digits in this column, form a number
        if number_digits:
            number = int(''.join(number_digits))
            current_problem_numbers.append(number)

        # If we found an operator, this marks the end of a problem
        if operator:
            # Calculate result for this problem
            if operator == '+':
                result = sum(current_problem_numbers)
            else:  # operator == '*'
                result = 1
                for num in current_problem_numbers:
                    result *= num

            grand_total += result
            current_problem_numbers = []  # Start new problem

    return grand_total


if __name__ == '__main__':
    # Test with the example
    simple_test = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

    with open('test_input.txt', 'w') as f:
        f.write(simple_test)

    result = solve_worksheet_part2('test_input.txt')
    print(f"Test result: {result}")
    print(f"Expected: 3263827")
    print()

    # Solve the actual puzzle
    result = solve_worksheet_part2('input.txt')
    print(f"Part 2 answer: {result}")
