const fs = require('fs');

// Read the input
const input = fs.readFileSync('input.txt', 'utf8').trim();
const grid = input.split('\n').map(line => line.split(''));

const rows = grid.length;
const cols = grid[0].length;

// Eight directions: N, NE, E, SE, S, SW, W, NW
const directions = [
  [-1, 0], [-1, 1], [0, 1], [1, 1],
  [1, 0], [1, -1], [0, -1], [-1, -1]
];

function countAdjacentRolls(row, col) {
  let count = 0;

  for (const [dr, dc] of directions) {
    const newRow = row + dr;
    const newCol = col + dc;

    // Check if the adjacent position is within bounds and has a roll
    if (newRow >= 0 && newRow < rows &&
        newCol >= 0 && newCol < cols &&
        grid[newRow][newCol] === '@') {
      count++;
    }
  }

  return count;
}

// Count accessible rolls
let accessibleCount = 0;

for (let row = 0; row < rows; row++) {
  for (let col = 0; col < cols; col++) {
    if (grid[row][col] === '@') {
      const adjacentRolls = countAdjacentRolls(row, col);

      // A roll is accessible if it has fewer than 4 adjacent rolls
      if (adjacentRolls < 4) {
        accessibleCount++;
      }
    }
  }
}

console.log(`Number of accessible rolls: ${accessibleCount}`);
