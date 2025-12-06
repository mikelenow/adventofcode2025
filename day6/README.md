# Day 6: Trash Compactor

## Part 1: Horizontal Reading

### Problem Summary
The challenge involves solving a series of math problems presented in an unusual horizontal format. Each problem consists of numbers arranged vertically across multiple rows, with an operator (+  or *) at the bottom.

### Input Format
- 4 rows of numbers (1000 numbers per row)
- 1 row of operators (1000 operators)
- Each column represents one problem

Example:
```
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
```

This represents 4 problems:
- Problem 1: 123 * 45 * 6 = 33210
- Problem 2: 328 + 64 + 98 = 490
- Problem 3: 51 * 387 * 215 = 4243455
- Problem 4: 64 + 23 + 314 = 401

### Part 1 Answer
**5733696195703**

## Part 2: Cephalopod Math (Vertical, Right-to-Left)

### Problem Summary
Cephalopod math is written right-to-left in columns. Each number is given in its own vertical column, with the most significant digit at the top and the least significant digit at the bottom.

### Reading Method (CRITICAL!)
Process columns from **right to left**, one column at a time:
1. For each column, read vertically (top-to-bottom) to collect digit characters
2. If digits are found, form a number and add it to the current problem
3. If an **operator** (+/*) is found in that column, it marks the **END of the current problem**:
   - Calculate the result using all accumulated numbers
   - Add result to grand total
   - Start a new problem
4. Continue processing columns left until all are processed

Example (same input, different interpretation):
```
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
```

Reading columns right-to-left (column 14 → 0):
- Col 14: digit '4', operator '+' → Problem: [4, 431, 623] + = 1058
- Col 13: digits '431' → accumulate
- Col 12: digits '623' → accumulate
- Col 11: (separator, skip)
- Col 10: digits '175' → accumulate
- Col 9: digits '581', operator '*' → Problem: [175, 581, 32] * = 3253600
- Col 8: digits '32' → accumulate
- ...and so on

Grand total: 3263827

### Part 2 Answer
**10951882745757**

## Files

- `input.txt` - Puzzle input
- `solution.py` - Part 1 Python solution
- `solution_part2.py` - Part 2 Python solution
- `answer.txt` - Part 1 answer
- `answer_part2.txt` - Part 2 answer
- `README.md` - This file
