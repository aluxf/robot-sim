import unittest
from robot import Direction


class TestDirection(unittest.TestCase):
    def test_rotate_left(self):
        self.assertEqual(Direction.rotate_left(Direction.NORTH), Direction.WEST)
        self.assertEqual(Direction.rotate_left(Direction.WEST), Direction.SOUTH)
        self.assertEqual(Direction.rotate_left(Direction.SOUTH), Direction.EAST)
        self.assertEqual(Direction.rotate_left(Direction.EAST), Direction.NORTH)

    def test_rotate_right(self):
        self.assertEqual(Direction.rotate_right(Direction.NORTH), Direction.EAST)
        self.assertEqual(Direction.rotate_right(Direction.EAST), Direction.SOUTH)
        self.assertEqual(Direction.rotate_right(Direction.SOUTH), Direction.WEST)
        self.assertEqual(Direction.rotate_right(Direction.WEST), Direction.NORTH)


if __name__ == '__main__':
    unittest.main()