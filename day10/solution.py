import re
from typing import List, Tuple, Set
import numpy as np
from scipy.optimize import linprog
from scipy.optimize import milp, LinearConstraint, Bounds

def parse_machine(line: str) -> Tuple[List[int], List[Set[int]], List[int]]:
    """Parse a machine configuration line.

    Returns:
        target: List of target states (0 or 1) for each light
        buttons: List of sets, each containing indices of lights the button toggles
        joltages: List of joltage requirements
    """
    # Extract indicator lights pattern [.##.]
    lights_match = re.search(r'\[(.*?)\]', line)
    if not lights_match:
        raise ValueError(f"No lights pattern found in: {line}")
    lights_str = lights_match.group(1)
    target = [1 if c == '#' else 0 for c in lights_str]

    # Extract all button configurations (0,3,4)
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for match in button_matches:
        indices = set(int(x) for x in match.split(','))
        buttons.append(indices)

    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltages = []
    if joltage_match:
        joltages = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, joltages

def solve_machine_bruteforce(target: List[int], buttons: List[Set[int]]) -> int:
    """Solve using brute force for small button counts.

    Try all possible combinations of button presses and return the minimum.
    """
    n_buttons = len(buttons)
    n_lights = len(target)

    if n_buttons > 20:
        # Too many combinations, fall back to GF(2) solution
        return solve_machine_gf2_simple(target, buttons)

    min_presses = float('inf')

    # Try all 2^n_buttons combinations
    for mask in range(1 << n_buttons):
        # Calculate resulting light state
        lights = [0] * n_lights
        presses = 0

        for button_idx in range(n_buttons):
            if mask & (1 << button_idx):
                presses += 1
                # Toggle lights for this button
                for light_idx in buttons[button_idx]:
                    lights[light_idx] = 1 - lights[light_idx]

        # Check if this matches target
        if lights == target:
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else -1

def solve_machine_gf2_simple(target: List[int], buttons: List[Set[int]]) -> int:
    """Simple GF(2) solver for when brute force is too expensive."""
    n_lights = len(target)
    n_buttons = len(buttons)

    # Build the matrix where each column represents a button
    matrix = []
    for light_idx in range(n_lights):
        row = []
        for button in buttons:
            row.append(1 if light_idx in button else 0)
        matrix.append(row)

    A = np.array(matrix, dtype=int)
    b = np.array(target, dtype=int).reshape(-1, 1)
    aug = np.hstack([A, b])

    rows, cols = aug.shape
    n_vars = cols - 1

    current_row = 0
    for col in range(n_vars):
        pivot_row = None
        for row in range(current_row, rows):
            if aug[row, col] % 2 == 1:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        if pivot_row != current_row:
            aug[[current_row, pivot_row]] = aug[[pivot_row, current_row]]

        for row in range(rows):
            if row != current_row and aug[row, col] % 2 == 1:
                aug[row] = (aug[row] + aug[current_row]) % 2

        current_row += 1

    for row in range(rows):
        if all(aug[row, :-1] % 2 == 0) and aug[row, -1] % 2 == 1:
            return -1

    solution = [0] * n_vars
    for row in range(min(current_row, rows) - 1, -1, -1):
        leading_col = None
        for col in range(n_vars):
            if aug[row, col] % 2 == 1:
                leading_col = col
                break

        if leading_col is None:
            continue

        val = aug[row, -1]
        for col in range(leading_col + 1, n_vars):
            val = (val - aug[row, col] * solution[col]) % 2
        solution[leading_col] = val % 2

    return sum(solution)

def solve_machine_joltage(joltages: List[int], buttons: List[Set[int]]) -> int:
    """Solve Part 2: find minimum button presses to reach joltage levels.

    This is an integer linear programming problem:
    - Minimize sum of button presses
    - Subject to: for each counter, sum of button presses must equal target joltage
    """
    n_counters = len(joltages)
    n_buttons = len(buttons)

    # Build constraint matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons), dtype=float)
    for counter_idx in range(n_counters):
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                A[counter_idx, button_idx] = 1.0

    # Target values
    b = np.array(joltages, dtype=float)

    # Objective: minimize sum of button presses (all coefficients are 1)
    c = np.ones(n_buttons)

    # Use scipy's milp for integer linear programming
    constraints = LinearConstraint(A, b, b)  # A*x == b
    bounds = Bounds(lb=0, ub=np.inf)  # x >= 0

    # Solve with integer constraints
    integrality = np.ones(n_buttons)  # All variables must be integers

    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        # Fallback: try linprog and round
        result_lp = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='highs')
        if result_lp.success:
            # Round to nearest integer and verify
            x = np.round(result_lp.x).astype(int)
            # Verify the solution
            if np.allclose(A @ x, b):
                return int(np.sum(x))
        return -1

def solve_part1(filename: str) -> int:
    """Solve part 1: find total minimum button presses for all machines."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_presses = 0
    for i, line in enumerate(lines):
        target, buttons, joltages = parse_machine(line)
        presses = solve_machine_bruteforce(target, buttons)
        if presses == -1:
            print(f"Machine {i+1}: No solution found!")
            return -1
        print(f"Machine {i+1}: {presses} presses needed")
        total_presses += presses

    return total_presses

def solve_part2(filename: str) -> int:
    """Solve part 2: find total minimum button presses for joltage configuration."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_presses = 0
    for i, line in enumerate(lines):
        target, buttons, joltages = parse_machine(line)
        presses = solve_machine_joltage(joltages, buttons)
        if presses == -1:
            print(f"Machine {i+1}: No solution found!")
            return -1
        print(f"Machine {i+1}: {presses} presses needed (joltages: {joltages})")
        total_presses += presses

    return total_presses

def test_example():
    """Test with the provided example."""
    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    lines = example.split('\n')

    # Test Part 1
    print("Part 1 - Indicator Lights:")
    total_part1 = 0
    for i, line in enumerate(lines):
        target, buttons, joltages = parse_machine(line)
        presses = solve_machine_bruteforce(target, buttons)
        print(f"  Machine {i+1}: {presses} presses (target: {target})")
        total_part1 += presses
    print(f"  Total: {total_part1} presses (Expected: 7)")

    # Test Part 2
    print("\nPart 2 - Joltage Levels:")
    total_part2 = 0
    for i, line in enumerate(lines):
        target, buttons, joltages = parse_machine(line)
        presses = solve_machine_joltage(joltages, buttons)
        print(f"  Machine {i+1}: {presses} presses (joltages: {joltages})")
        total_part2 += presses
    print(f"  Total: {total_part2} presses (Expected: 33)")

    return total_part1, total_part2

if __name__ == "__main__":
    # Test with example first
    print("=== Testing with example ===")
    test_example()

    print("\n" + "="*50)
    print("=== Solving actual input ===")
    print("="*50)

    try:
        print("\n--- Part 1: Indicator Lights ---")
        result1 = solve_part1('input.txt')
        if result1 != -1:
            print(f"\nPart 1 Answer: {result1}")

        print("\n--- Part 2: Joltage Levels ---")
        result2 = solve_part2('input.txt')
        if result2 != -1:
            print(f"\nPart 2 Answer: {result2}")

    except FileNotFoundError:
        print("input.txt not found or empty")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
