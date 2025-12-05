const fs = require('fs');

// Read input
const input = fs.readFileSync('input.txt', 'utf8').trim();
const banks = input.split('\n');

let totalJoltage = 0n; // Use BigInt for large numbers

for (const bank of banks) {
    const n = bank.length;
    const digitsToSelect = 12;

    let result = '';
    let lastPos = -1;

    // For each position in our 12-digit result
    for (let k = 0; k < digitsToSelect; k++) {
        const digitsRemaining = digitsToSelect - k;
        const startPos = lastPos + 1;
        const endPos = n - digitsRemaining;

        // Find the maximum digit in the valid range [startPos, endPos]
        // If there are multiple occurrences of the max, pick the leftmost
        let maxDigit = -1;
        let maxPos = -1;

        for (let pos = startPos; pos <= endPos; pos++) {
            const digit = parseInt(bank[pos]);
            if (digit > maxDigit) {
                maxDigit = digit;
                maxPos = pos;
            }
        }

        result += maxDigit;
        lastPos = maxPos;
    }

    totalJoltage += BigInt(result);
}

console.log('Total output joltage:', totalJoltage.toString());
