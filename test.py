import random
import unittest
from robot import Direction, Environment, Position, Robot


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



class TestPosition(unittest.TestCase):
    def test_update(self):
        pos = Position(0, 0)
        pos.update(1, 1)
        self.assertEqual(pos.x, 1)
        self.assertEqual(pos.y, 1)

    def test_random_update(self):
        pos = Position(0, 0)

        # Test 10 random updates
        for _ in range(10):
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            pos.update(x, y)
            self.assertEqual(pos.x, x)
            self.assertEqual(pos.y, y)

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.env = Environment(5, 5)
        self.robot = Robot(environment=self.env)

    def test_place(self):
        # Test valid position
        self.assertTrue(self.robot.place(1, 1, Direction.NORTH))
        self.assertEqual(self.robot.position.x, 1)
        self.assertEqual(self.robot.position.y, 1)
        self.assertEqual(self.robot.f, Direction.NORTH)

        # Test invalid position
        self.assertFalse(self.robot.place(5, 5, Direction.SOUTH))

        # Check position not updated
        self.assertEqual(self.robot.position.x, 1)
        self.assertEqual(self.robot.position.y, 1)
        self.assertEqual(self.robot.f, Direction.NORTH)

    def test_move(self):
         # Valid NORTH move
        self.robot.place(1, 1, Direction.NORTH)
        self.assertTrue(self.robot.move())
        self.assertEqual(self.robot.position.x, 1)
        self.assertEqual(self.robot.position.y, 2)

        # Valid EAST move
        self.robot.place(1, 1, Direction.EAST)
        self.assertTrue(self.robot.move())
        self.assertEqual(self.robot.position.x, 2)
        self.assertEqual(self.robot.position.y, 1)

        # Valid SOUTH move
        self.robot.place(1, 1, Direction.SOUTH)
        self.assertTrue(self.robot.move())
        self.assertEqual(self.robot.position.x, 1)
        self.assertEqual(self.robot.position.y, 0)

        # Valid WEST move
        self.robot.place(1, 1, Direction.WEST)
        self.assertTrue(self.robot.move())
        self.assertEqual(self.robot.position.x, 0)
        self.assertEqual(self.robot.position.y, 1)

        # Invalid NORTH move (out of bounds)
        self.robot.place(0, 4, Direction.NORTH)
        self.assertFalse(self.robot.move())
        self.assertEqual(self.robot.position.x, 0)
        self.assertEqual(self.robot.position.y, 4)

        # Invalid EAST move (out of bounds)
        self.robot.place(4, 0, Direction.EAST)
        self.assertFalse(self.robot.move())
        self.assertEqual(self.robot.position.x, 4)
        self.assertEqual(self.robot.position.y, 0)

        # Invalid SOUTH move (out of bounds)
        self.robot.place(0, 0, Direction.SOUTH)
        self.assertFalse(self.robot.move())
        self.assertEqual(self.robot.position.x, 0)
        self.assertEqual(self.robot.position.y, 0)

        # Invalid WEST move (out of bounds)
        self.robot.place(0, 0, Direction.WEST)
        self.assertFalse(self.robot.move())
        self.assertEqual(self.robot.position.x, 0)
        self.assertEqual(self.robot.position.y, 0)

    def test_rotate(self):
        # Full 360 LEFT rotation
        self.robot.place(0, 0, Direction.NORTH)
        self.robot.rotate("LEFT")
        self.assertEqual(self.robot.f, Direction.WEST)
        self.robot.rotate("LEFT")
        self.assertEqual(self.robot.f, Direction.SOUTH)
        self.robot.rotate("LEFT")
        self.assertEqual(self.robot.f, Direction.EAST)
        self.robot.rotate("LEFT")
        self.assertEqual(self.robot.f, Direction.NORTH)

        # Full 360 RIGHT rotation
        self.robot.place(0, 0, Direction.NORTH)
        self.robot.rotate("RIGHT")
        self.assertEqual(self.robot.f, Direction.EAST)
        self.robot.rotate("RIGHT")
        self.assertEqual(self.robot.f, Direction.SOUTH)
        self.robot.rotate("RIGHT")
        self.assertEqual(self.robot.f, Direction.WEST)
        self.robot.rotate("RIGHT")
        self.assertEqual(self.robot.f, Direction.NORTH)

    def test_report(self):
        self.robot.place(1, 1, Direction.NORTH)
        
        report_message = self.robot.report()
        self.assertEqual(report_message, "Report: 1,1,NORTH")
        

if __name__ == '__main__':
    unittest.main()