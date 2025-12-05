const fs = require('fs');
const content = fs.readFileSync('day5_input.txt', 'utf-8');
const lines = content.trim().split('\n');

let ranges = [];
for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed === '') break;
    const [start, end] = trimmed.split('-').map(Number);
    ranges.push({ start, end });
}

console.log('Original ranges:', ranges.length);

// Sort
ranges.sort((a, b) => a.start - b.start);

// Merge
const merged = [ranges[0]];
for (let i = 1; i < ranges.length; i++) {
    const current = ranges[i];
    const last = merged[merged.length - 1];

    if (current.start <= last.end + 1) {
        last.end = Math.max(last.end, current.end);
    } else {
        merged.push(current);
    }
}

console.log('Merged ranges:', merged.length);
console.log('\nAll merged ranges:');
merged.forEach((r, i) => {
    const count = r.end - r.start + 1;
    console.log(`${i+1}. ${r.start}-${r.end} (${count} IDs)`);
});

let total = 0;
for (const range of merged) {
    total += (range.end - range.start + 1);
}
console.log('\nTotal IDs:', total);
