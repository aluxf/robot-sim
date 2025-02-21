import unittest
from robot import Direction, Environment


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

class TestEnvironment(unittest.TestCase):
    def test_is_valid_position(self):

        # For clarity
        x_max = 4
        y_max = 4
        x_min = 0
        y_min = 0

        # Test with 5x5 environment
        env = Environment(x_max+1, y_max+1)

        # TODO: Test all valid positions?
        self.assertTrue(env.is_valid_position(0, 0))
        self.assertTrue(env.is_valid_position(4, 4))

        # X > X_max and Y > y_max
        self.assertFalse(env.is_valid_position(x_max+1, y_max+1))

        # X < x_min and Y < y_min
        self.assertFalse(env.is_valid_position(x_min-1, y_min-1))

        # X < x_min and Y > y_max
        self.assertFalse(env.is_valid_position(x_min-1, y_max+1))

        # X > x_max and Y < y_min
        self.assertFalse(env.is_valid_position(x_max+1, y_min-1))

        # X < x_min
        self.assertFalse(env.is_valid_position(x_min-1, 4))

        # Y < y_min
        self.assertFalse(env.is_valid_position(4, y_min-1))

        # X > x_max
        self.assertFalse(env.is_valid_position(x_max+1, 4))

        # Y > y_max
        self.assertFalse(env.is_valid_position(4, y_max+1))

if __name__ == '__main__':
    unittest.main()