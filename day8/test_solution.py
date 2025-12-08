import unittest
from solution import parse_input, find_antennas, find_antinodes

class TestDay8(unittest.TestCase):
    def setUp(self):
        self.grid = parse_input('test_input.txt')

    def test_parse_input(self):
        """Test that input is parsed correctly."""
        self.assertEqual(len(self.grid), 12)
        self.assertEqual(len(self.grid[0]), 12)

    def test_find_antennas(self):
        """Test that antennas are found and grouped correctly."""
        antennas = find_antennas(self.grid)
        self.assertIn('0', antennas)
        self.assertIn('A', antennas)
        self.assertEqual(len(antennas['0']), 4)
        self.assertEqual(len(antennas['A']), 3)

    def test_find_antinodes(self):
        """Test that the correct number of antinodes are found."""
        antinodes = find_antinodes(self.grid)
        self.assertEqual(len(antinodes), 14)

    def test_antenna_positions(self):
        """Verify specific antenna positions from the example."""
        antennas = find_antennas(self.grid)
        # Check frequency '0' positions
        self.assertIn((1, 8), antennas['0'])
        self.assertIn((2, 5), antennas['0'])
        self.assertIn((3, 7), antennas['0'])
        self.assertIn((4, 4), antennas['0'])
        # Check frequency 'A' positions
        self.assertIn((5, 6), antennas['A'])
        self.assertIn((8, 8), antennas['A'])
        self.assertIn((9, 9), antennas['A'])

if __name__ == '__main__':
    unittest.main()
