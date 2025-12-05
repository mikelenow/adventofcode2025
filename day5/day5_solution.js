#!/usr/bin/env node

/**
 * Advent of Code - Day 5: Cafeteria
 * Checks which available ingredient IDs are fresh based on fresh ID ranges
 */

const fs = require('fs');
const path = require('path');

/**
 * Parse the database file into ranges and available IDs
 * @param {string} content - The file content
 * @returns {{ranges: Array<{start: number, end: number}>, ids: number[]}}
 */
function parseDatabase(content) {
    const lines = content.trim().split('\n');
    const ranges = [];
    const ids = [];
    let parsingRanges = true;

    for (const line of lines) {
        const trimmed = line.trim();

        // Empty line separates ranges from IDs
        if (trimmed === '') {
            parsingRanges = false;
            continue;
        }

        if (parsingRanges) {
            // Parse range like "3-5"
            const [start, end] = trimmed.split('-').map(Number);
            ranges.push({ start, end });
        } else {
            // Parse individual ID
            ids.push(Number(trimmed));
        }
    }

    return { ranges, ids };
}

/**
 * Check if an ID is fresh (falls within any range)
 * @param {number} id - The ingredient ID to check
 * @param {Array<{start: number, end: number}>} ranges - Array of fresh ranges
 * @returns {boolean}
 */
function isFresh(id, ranges) {
    return ranges.some(range => id >= range.start && id <= range.end);
}

/**
 * Count how many available ingredient IDs are fresh
 * @param {string} content - The database content
 * @returns {number}
 */
function countFreshIngredients(content) {
    const { ranges, ids } = parseDatabase(content);

    let freshCount = 0;
    const details = [];

    for (const id of ids) {
        const fresh = isFresh(id, ranges);
        freshCount += fresh ? 1 : 0;
        details.push(`Ingredient ID ${id} is ${fresh ? 'fresh' : 'spoiled'}`);
    }

    // Print details
    details.forEach(detail => console.log(detail));

    return freshCount;
}

// Example test
const exampleInput = `3-5
10-14
16-20
12-18

1
5
8
11
17
32`;

console.log('=== Testing with Example ===');
const exampleResult = countFreshIngredients(exampleInput);
console.log(`\nResult: ${exampleResult} fresh ingredients\n`);

// Process actual input file if provided
const inputFile = process.argv[2] || 'day5_input.txt';
const inputPath = path.join(__dirname, inputFile);

if (fs.existsSync(inputPath)) {
    console.log('=== Processing Actual Input ===');
    const actualInput = fs.readFileSync(inputPath, 'utf-8');
    const actualResult = countFreshIngredients(actualInput);
    console.log(`\n**Answer: ${actualResult} fresh ingredients**`);
} else {
    console.log(`\nNo input file found at ${inputPath}`);
    console.log('To use with your puzzle input:');
    console.log(`  1. Save your puzzle input to ${inputFile}`);
    console.log(`  2. Run: node day5_solution.js`);
}
