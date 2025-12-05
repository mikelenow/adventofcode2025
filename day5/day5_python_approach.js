const fs = require('fs');

// Parse ranges
const fresh = [];
const lines = fs.readFileSync('day5_input.txt', 'utf-8').split('\n');

for (const line of lines) {
    if (line.trim() === '') break;
    const [left, right] = line.split('-').map(Number);
    fresh.push([left, right]);
}

console.log('Parsed ranges:', fresh.length);

// First pass: merge ranges
const tested = [];
for (const [left, right] of fresh) {
    let merged = false;

    for (let i = 0; i < tested.length; i++) {
        const [tleft, tright] = tested[i];

        if (tleft <= left && left <= tright) {
            if (right > tright) {
                tested[i][1] = right;
            }
            merged = true;
            break;
        }
        if (tleft <= right && right <= tright) {
            if (left < tleft) {
                tested[i][0] = left;
            }
            merged = true;
            break;
        }
    }

    if (!merged) {
        tested.push([left, right]);
    }
}

console.log('After first merge:', tested.length);

// "time to break bridges" - remove overlaps
for (let i = 0; i < tested.length; i++) {
    for (let j = 0; j < tested.length; j++) {
        if (i !== j) {
            // If range i's start is within range j, move it past range j
            if (tested[j][0] <= tested[i][0] && tested[i][0] <= tested[j][1]) {
                tested[i][0] = tested[j][1] + 1;
            }
            // If range i's end is within range j, move it before range j
            if (tested[j][0] <= tested[i][1] && tested[i][1] <= tested[j][1]) {
                tested[i][1] = tested[j][0] - 1;
            }
        }
    }
}

console.log('After breaking bridges:', tested.length);

// Count total
let total = 0;
for (const [left, right] of tested) {
    if (right >= left) {
        total += (right - left + 1);
    }
}

console.log('Total IDs:', total);
