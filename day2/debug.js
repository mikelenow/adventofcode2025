/**
 * Debug script to verify individual cases
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
        if (len % patternLen === 0) {
            const pattern = str.slice(0, patternLen);
            const repetitions = len / patternLen;
            const repeated = pattern.repeat(repetitions);

            if (repeated === str && repetitions >= 2) {
                console.log(`  ${num}: "${pattern}" × ${repetitions}`);
                return true;
            }
        }
    }

    return false;
}

// Test cases from the problem
console.log('Part 1 (exactly twice):');
console.log('11:', isInvalidId(11, true)); // should be true (1 twice)
console.log('99:', isInvalidId(99, true)); // should be true (9 twice)
console.log('111:', isInvalidId(111, true)); // should be false (1 three times, not exactly twice)
console.log('1010:', isInvalidId(1010, true)); // should be true (10 twice)

console.log('\nPart 2 (at least twice):');
console.log('11:', isInvalidId(11, false)); // should be true
console.log('99:', isInvalidId(99, false)); // should be true
console.log('111:', isInvalidId(111, false)); // should be true (1 three times)
console.log('999:', isInvalidId(999, false)); // should be true (9 three times)
console.log('1010:', isInvalidId(1010, false)); // should be true
console.log('565656:', isInvalidId(565656, false)); // should be true (56 three times)
console.log('824824824:', isInvalidId(824824824, false)); // should be true (824 three times)
console.log('2121212121:', isInvalidId(2121212121, false)); // should be true (21 five times)
