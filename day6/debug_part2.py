def solve_worksheet_part2_debug(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    operator_line = lines[-1]
    number_lines = lines[:-1]

    # Find separator columns
    is_separator = [all(line[col] == ' ' for line in lines) for col in range(max_len)]

    # Group into problems
    problems = []
    current_problem = []
    for col in range(max_len):
        if is_separator[col]:
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(col)
    if current_problem:
        problems.append(current_problem)

    # Try different approaches
    results = {}

    # Approach 1: Process problems right-to-left, columns within problem right-to-left
    grand_total = 0
    for problem_cols in reversed(problems):
        operator = None
        for col in reversed(problem_cols):
            if operator_line[col] in ['+', '*']:
                operator = operator_line[col]
                break
        if operator is None:
            continue
        numbers = []
        for col in reversed(problem_cols):
            digits = [row[col] for row in number_lines if row[col] != ' ']
            if digits:
                numbers.append(int(''.join(digits)))
        result = sum(numbers) if operator == '+' else eval('*'.join(map(str, numbers)))
        grand_total += result
    results['R-to-L problems, R-to-L columns'] = grand_total

    # Approach 2: Process problems right-to-left, columns within problem left-to-right
    grand_total = 0
    for problem_cols in reversed(problems):
        operator = None
        for col in problem_cols:  # Changed: not reversed
            if operator_line[col] in ['+', '*']:
                operator = operator_line[col]
                break
        if operator is None:
            continue
        numbers = []
        for col in problem_cols:  # Changed: not reversed
            digits = [row[col] for row in number_lines if row[col] != ' ']
            if digits:
                numbers.append(int(''.join(digits)))
        result = sum(numbers) if operator == '+' else eval('*'.join(map(str, numbers)))
        grand_total += result
    results['R-to-L problems, L-to-R columns'] = grand_total

    # Approach 3: Process problems left-to-right, columns within problem right-to-left
    grand_total = 0
    for problem_cols in problems:  # Changed: not reversed
        operator = None
        for col in reversed(problem_cols):
            if operator_line[col] in ['+', '*']:
                operator = operator_line[col]
                break
        if operator is None:
            continue
        numbers = []
        for col in reversed(problem_cols):
            digits = [row[col] for row in number_lines if row[col] != ' ']
            if digits:
                numbers.append(int(''.join(digits)))
        result = sum(numbers) if operator == '+' else eval('*'.join(map(str, numbers)))
        grand_total += result
    results['L-to-R problems, R-to-L columns'] = grand_total

    # Approach 4: Process problems left-to-right, columns within problem left-to-right
    grand_total = 0
    for problem_cols in problems:  # Changed: not reversed
        operator = None
        for col in problem_cols:  # Changed: not reversed
            if operator_line[col] in ['+', '*']:
                operator = operator_line[col]
                break
        if operator is None:
            continue
        numbers = []
        for col in problem_cols:  # Changed: not reversed
            digits = [row[col] for row in number_lines if row[col] != ' ']
            if digits:
                numbers.append(int(''.join(digits)))
        result = sum(numbers) if operator == '+' else eval('*'.join(map(str, numbers)))
        grand_total += result
    results['L-to-R problems, L-to-R columns'] = grand_total

    return results


# Test with example
simple_test = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

with open('test_input.txt', 'w') as f:
    f.write(simple_test)

print("Test case results:")
test_results = solve_worksheet_part2_debug('test_input.txt')
for approach, result in test_results.items():
    status = "✓" if result == 3263827 else "✗"
    print(f"{status} {approach}: {result}")

print("\nActual input results:")
actual_results = solve_worksheet_part2_debug('input.txt')
for approach, result in actual_results.items():
    print(f"{approach}:")
    print(f"  {result}")
    print()
