const fs = require('fs');

// Read input
const input = fs.readFileSync('input.txt', 'utf8').trim();
const banks = input.split('\n');

let totalJoltage = 0;

for (const bank of banks) {
    let maxJoltage = 0;

    // Try all pairs of positions (i, j) where i < j
    // We need to find the maximum 2-digit number formed by digits at positions i and j
    for (let i = 0; i < bank.length; i++) {
        for (let j = i + 1; j < bank.length; j++) {
            const joltage = parseInt(bank[i]) * 10 + parseInt(bank[j]);
            maxJoltage = Math.max(maxJoltage, joltage);
        }
    }

    totalJoltage += maxJoltage;
}

console.log('Total output joltage:', totalJoltage);
