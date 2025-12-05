const fs = require('fs');

// Read the input
const input = fs.readFileSync('input.txt', 'utf8').trim();
let grid = input.split('\n').map(line => line.split(''));

const rows = grid.length;
const cols = grid[0].length;

// Eight directions: N, NE, E, SE, S, SW, W, NW
const directions = [
  [-1, 0], [-1, 1], [0, 1], [1, 1],
  [1, 0], [1, -1], [0, -1], [-1, -1]
];

function countAdjacentRolls(row, col, currentGrid) {
  let count = 0;

  for (const [dr, dc] of directions) {
    const newRow = row + dr;
    const newCol = col + dc;

    // Check if the adjacent position is within bounds and has a roll
    if (newRow >= 0 && newRow < rows &&
        newCol >= 0 && newCol < cols &&
        currentGrid[newRow][newCol] === '@') {
      count++;
    }
  }

  return count;
}

function findAccessibleRolls(currentGrid) {
  const accessible = [];

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (currentGrid[row][col] === '@') {
        const adjacentRolls = countAdjacentRolls(row, col, currentGrid);

        // A roll is accessible if it has fewer than 4 adjacent rolls
        if (adjacentRolls < 4) {
          accessible.push([row, col]);
        }
      }
    }
  }

  return accessible;
}

function removeRolls(currentGrid, rollsToRemove) {
  // Create a copy of the grid
  const newGrid = currentGrid.map(row => [...row]);

  // Remove all accessible rolls
  for (const [row, col] of rollsToRemove) {
    newGrid[row][col] = '.';
  }

  return newGrid;
}

// Simulate the removal process
let totalRemoved = 0;
let currentGrid = grid;
let iteration = 0;

while (true) {
  const accessible = findAccessibleRolls(currentGrid);

  if (accessible.length === 0) {
    break; // No more rolls can be removed
  }

  iteration++;
  console.log(`Iteration ${iteration}: Removing ${accessible.length} rolls`);

  totalRemoved += accessible.length;
  currentGrid = removeRolls(currentGrid, accessible);
}

console.log(`\nTotal rolls removed: ${totalRemoved}`);
