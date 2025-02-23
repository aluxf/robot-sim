from contextlib import redirect_stdout
import io
import os
import random
import unittest
from robot import Direction, Environment, Interface, Position, Robot


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

class TestInterface(unittest.TestCase):
    def setUp(self):
        self.env = Environment(5, 5)
        self.robot = Robot(environment=self.env)
        self.interface = Interface(robot=self.robot)

    # is_command_prohibited tests
    def test_is_command_prohibited(self):
        # Test before valid PLACE command
        self.assertTrue(self.interface.is_command_prohibited("MOVE"))
        self.assertTrue(self.interface.is_command_prohibited("LEFT"))
        self.assertTrue(self.interface.is_command_prohibited("RIGHT"))
        self.assertTrue(self.interface.is_command_prohibited("REPORT"))

        self.assertFalse(self.interface.is_command_prohibited("PLACE"))

        # Test after valid PLACE command
        self.interface.parse_command("PLACE,1,1,NORTH")
        self.assertFalse(self.interface.is_command_prohibited("MOVE"))
        self.assertFalse(self.interface.is_command_prohibited("LEFT"))
        self.assertFalse(self.interface.is_command_prohibited("RIGHT"))
        self.assertFalse(self.interface.is_command_prohibited("REPORT"))
        self.assertFalse(self.interface.is_command_prohibited("PLACE"))

    # parse_command tests

    # TODO: Test all possible valid positions?
    def test_parse_command_place(self):
        try:
            self.interface.parse_command("PLACE,1,1,NORTH")
            self.interface.parse_command("PLACE,4,1,SOUTH")
            self.interface.parse_command("PLACE,2,2,EAST")
            self.interface.parse_command("PLACE,1,1,WEST")
        except Exception as e:
            self.fail(e)
    
    def test_parse_command_invalid_place_arguments(self):
        # Missing arguments
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE")

        # Missing direction
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE,1,1,")

        # Missing direction and y
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE,1,,")

        # Missing direction and x and y
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE,,,")

        # Invalid types
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE,x,y,1")
        
        # Invalid direction
        with self.assertRaises(ValueError):
            self.interface.parse_command("PLACE,1,1,UP")
            self.interface.parse_command("PLACE,1,1,NORT")

    def test_parse_command_without_place(self):
        with self.assertRaises(ValueError):
            self.interface.parse_command("LEFT")
        
        with self.assertRaises(ValueError):
            self.interface.parse_command("RIGHT")

        with self.assertRaises(ValueError):
            self.interface.parse_command("MOVE")
        
        with self.assertRaises(ValueError):
            self.interface.parse_command("REPORT")

    def test_parse_command_with_place(self):
        self.interface.parse_command("PLACE,1,1,NORTH")
        try:
            self.interface.parse_command("REPORT")
            self.interface.parse_command("LEFT")
            self.interface.parse_command("RIGHT")
            self.interface.parse_command("MOVE")
        except Exception as e:
            self.fail(e)

    def test_parse_command_report(self):
        self.interface.parse_command("PLACE,1,1,NORTH")
        try:
            self.interface.parse_command("REPORT")
        except Exception as e:
            self.fail(e)

    def test_parse_command_rotate_left(self):
        self.interface.parse_command("PLACE,1,1,NORTH")
        try:
            self.interface.parse_command("LEFT")
        except Exception as e:
            self.fail(e)

    def test_parse_command_rotate_right(self):
        self.interface.parse_command("PLACE,1,1,NORTH")
        try:
            self.interface.parse_command("RIGHT")
        except Exception as e:
            self.fail(e)

    def test_parse_command_move(self):
        self.interface.parse_command("PLACE,1,1,NORTH")
        try:
            self.interface.parse_command("MOVE")
        except Exception as e:
            self.fail(e)

    def test_parse_command_invalid_command(self):
        with self.assertRaises(ValueError):
            self.interface.parse_command("JUMP")


class TestFileIntegration(unittest.TestCase):
    def test_integration_files(self):
        test_dir = "robot_tests"
        input_files = [f for f in os.listdir(test_dir) if f.endswith("_input.txt")]
        # Sort tests
        input_files.sort()
        
        for input_file in input_files:
            with self.subTest(test_file=input_file):
                input_path = os.path.join(test_dir, input_file)
                # The expected output file has same name with "_expected.txt"
                expected_path = os.path.join(test_dir, input_file.replace("_input.txt", "_expected.txt"))
                
                # Read all commands from the input file
                with open(input_path, "r") as f:
                    commands = f.read().splitlines()
                
                env = Environment(5, 5)
                robot = Robot(environment=env)
                interface = Interface(robot=robot)
                
                # Capture any printed output (from REPORT commands)
                output_capture = io.StringIO()
                with redirect_stdout(output_capture):
                    for command in commands:
                        if command.strip():
                            interface.execute(command)
                
                actual_output = output_capture.getvalue().strip().split('\n')[-1]

                
                # Read the expected output for comparison
                with open(expected_path, "r") as f:
                    expected_output = f.read().strip()
                
                self.assertEqual(actual_output, expected_output,
                                 f"Failed test file: {input_file}")

if __name__ == '__main__':
    unittest.main()