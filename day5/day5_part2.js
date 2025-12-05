#!/usr/bin/env node

/**
 * Advent of Code - Day 5 Part 2: Cafeteria
 * Count total unique ingredient IDs considered fresh across all ranges
 */

const fs = require('fs');
const path = require('path');

/**
 * Parse the database file to extract ranges
 * @param {string} content - The file content
 * @returns {Array<{start: number, end: number}>}
 */
function parseRanges(content) {
    const lines = content.trim().split('\n');
    const ranges = [];

    for (const line of lines) {
        const trimmed = line.trim();

        // Empty line signals end of ranges section
        if (trimmed === '') break;

        // Parse range like "3-5"
        const [start, end] = trimmed.split('-').map(Number);
        ranges.push({ start, end });
    }

    return ranges;
}

/**
 * Merge overlapping ranges and return merged list
 * @param {Array<{start: number, end: number}>} ranges - Array of ranges
 * @returns {Array<{start: number, end: number}>}
 */
function mergeRanges(ranges) {
    if (ranges.length === 0) return [];

    // Sort ranges by start position
    const sorted = [...ranges].sort((a, b) => a.start - b.start);

    const merged = [sorted[0]];

    for (let i = 1; i < sorted.length; i++) {
        const current = sorted[i];
        const last = merged[merged.length - 1];

        // Check if ranges overlap or are adjacent
        // Ranges overlap if current.start <= last.end + 1
        if (current.start <= last.end + 1) {
            // Merge by extending the end if necessary
            last.end = Math.max(last.end, current.end);
        } else {
            // No overlap, add as new range
            merged.push(current);
        }
    }

    return merged;
}

/**
 * Count total unique IDs across all ranges
 * @param {Array<{start: number, end: number}>} ranges - Array of ranges
 * @returns {number}
 */
function countTotalFreshIds(ranges) {
    const merged = mergeRanges(ranges);

    let total = 0;
    for (const range of merged) {
        // Inclusive range: end - start + 1
        total += (range.end - range.start + 1);
    }

    return total;
}

/**
 * Solve Part 2
 * @param {string} content - The database content
 * @returns {number}
 */
function solvePart2(content) {
    const ranges = parseRanges(content);
    console.log(`Parsed ${ranges.length} fresh ingredient ID ranges`);

    const totalIds = countTotalFreshIds(ranges);
    return totalIds;
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
const exampleRanges = parseRanges(exampleInput);
console.log('Ranges:', exampleRanges);
const merged = mergeRanges(exampleRanges);
console.log('Merged ranges:', merged);
const exampleResult = solvePart2(exampleInput);
console.log(`Result: ${exampleResult} fresh ingredient IDs\n`);

// Process actual input file
const inputFile = process.argv[2] || 'day5_input.txt';
const inputPath = path.join(__dirname, inputFile);

if (fs.existsSync(inputPath)) {
    console.log('=== Processing Actual Input ===');
    const actualInput = fs.readFileSync(inputPath, 'utf-8');
    const actualResult = solvePart2(actualInput);
    console.log(`\n**Answer: ${actualResult} fresh ingredient IDs**`);
} else {
    console.log(`\nNo input file found at ${inputPath}`);
}
