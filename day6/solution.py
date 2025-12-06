def solve_worksheet(filename):
    # Read the input
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # The last line contains operators, the rest contain numbers
    operator_line = lines[-1]
    number_lines = lines[:-1]

    # Split each line by whitespace to get the individual numbers/operators
    operators = operator_line.split()
    number_rows = [line.split() for line in number_lines]

    # Verify all rows have the same length
    num_problems = len(operators)
    print(f"Number of problems: {num_problems}")
    for i, row in enumerate(number_rows):
        if len(row) != num_problems:
            print(f"Warning: Row {i} has {len(row)} numbers, expected {num_problems}")

    # Solve each problem
    grand_total = 0

    for prob_idx in range(num_problems):
        operator = operators[prob_idx]

        # Get the numbers for this problem (one from each row)
        numbers = []
        for row in number_rows:
            numbers.append(int(row[prob_idx]))

        # Calculate result
        if operator == '+':
            result = sum(numbers)
        else:  # operator == '*'
            result = 1
            for num in numbers:
                result *= num

        grand_total += result

    return grand_total


if __name__ == '__main__':
    # Test with the simple example from the problem description
    simple_test = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

    with open('test_input.txt', 'w') as f:
        f.write(simple_test)

    result = solve_worksheet('test_input.txt')
    print(f"Simple test result: {result}")
    print(f"Expected: 4277556")
    print()

    # Now solve the actual puzzle input
    result = solve_worksheet('input.txt')
    print(f"Grand total: {result}")
