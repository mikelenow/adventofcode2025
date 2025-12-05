/**
 * Advent of Code 2025 - Day 2: Gift Shop
 * Find invalid product IDs (numbers that are digit sequences repeated twice)
 */

const fs = require('fs');
const path = require('path');

/**
 * Check if a number is an invalid ID (digit sequence repeated at least twice)
 * @param {number} num - The number to check
 * @param {boolean} exactlyTwice - If true, check for exactly twice; if false, at least twice
 * @returns {boolean} - True if the number is invalid
 */
function isInvalidId(num, exactlyTwice = false) {
    const str = num.toString();
    const len = str.length;

    if (exactlyTwice) {
        // Part 1: Must have even length and be exactly two repetitions
        if (len % 2 !== 0) {
            return false;
        }
        const mid = len / 2;
        const firstHalf = str.slice(0, mid);
        const secondHalf = str.slice(mid);
        return firstHalf === secondHalf;
    }

    // Part 2: Try all possible pattern lengths from 1 to len/2
    for (let patternLen = 1; patternLen <= len / 2; patternLen++) {
        // Check if the string length is divisible by the pattern length
        if (len % patternLen === 0) {
            const pattern = str.slice(0, patternLen);
            const repetitions = len / patternLen;

            // Build what the string should be if it's this pattern repeated
            const repeated = pattern.repeat(repetitions);

            if (repeated === str && repetitions >= 2) {
                return true;
            }
        }
    }

    return false;
}

/**
 * Parse ranges from input string
 * @param {string} input - The input string with ranges
 * @returns {Array<{start: number, end: number}>} - Array of range objects
 */
function parseRanges(input) {
    const ranges = [];
    const parts = input.trim().split(',');

    for (const part of parts) {
        const [start, end] = part.trim().split('-').map(Number);
        ranges.push({ start, end });
    }

    return ranges;
}

/**
 * Find all invalid IDs in a range
 * @param {number} start - Start of range
 * @param {number} end - End of range
 * @param {boolean} exactlyTwice - If true, check for exactly twice; if false, at least twice
 * @returns {number[]} - Array of invalid IDs
 */
function findInvalidIdsInRange(start, end, exactlyTwice = false) {
    const invalidIds = [];

    for (let id = start; id <= end; id++) {
        if (isInvalidId(id, exactlyTwice)) {
            invalidIds.push(id);
        }
    }

    return invalidIds;
}

/**
 * Solve the puzzle
 * @param {string} input - The puzzle input
 * @param {boolean} exactlyTwice - If true, check for exactly twice; if false, at least twice
 * @param {boolean} verbose - If true, print details for each range
 * @returns {number} - Sum of all invalid IDs
 */
function solve(input, exactlyTwice = false, verbose = false) {
    const ranges = parseRanges(input);
    let totalSum = 0;

    console.log(`Processing ${ranges.length} ranges...`);

    for (const range of ranges) {
        const invalidIds = findInvalidIdsInRange(range.start, range.end, exactlyTwice);
        const rangeSum = invalidIds.reduce((sum, id) => sum + id, 0);

        if (invalidIds.length > 0 && verbose) {
            console.log(`Range ${range.start}-${range.end}: Found ${invalidIds.length} invalid IDs: ${invalidIds.join(', ')}`);
        }

        totalSum += rangeSum;
    }

    return totalSum;
}

// Test with example
const exampleInput = `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124`;

console.log('='.repeat(60));
console.log('PART 1: Exactly twice repeated');
console.log('='.repeat(60));
console.log('\nTesting with example:');
const exampleResult1 = solve(exampleInput, true, false);
console.log(`Example result: ${exampleResult1}`);
console.log(`Expected: 1227775554`);
console.log(`Match: ${exampleResult1 === 1227775554 ? '✓' : '✗'}`);

// Solve Part 1 with actual input
try {
    const inputPath = path.join(__dirname, 'input.txt');
    const actualInput = fs.readFileSync(inputPath, 'utf8');

    console.log('\nSolving Part 1 with actual input:');
    const actualResult1 = solve(actualInput, true, false);
    console.log(`⭐ Part 1 Answer: ${actualResult1}`);

    console.log('\n' + '='.repeat(60));
    console.log('PART 2: At least twice repeated');
    console.log('='.repeat(60));
    console.log('\nTesting with example:');
    const exampleResult2 = solve(exampleInput, false, false);
    console.log(`Example result: ${exampleResult2}`);
    console.log(`Expected: 4174379265`);
    console.log(`Match: ${exampleResult2 === 4174379265 ? '✓' : '✗'}`);

    console.log('\nSolving Part 2 with actual input:');
    const actualResult2 = solve(actualInput, false, false);
    console.log(`⭐ Part 2 Answer: ${actualResult2}`);

} catch (err) {
    console.log('\nNo input.txt file found. Please create one with your puzzle input.');
}
