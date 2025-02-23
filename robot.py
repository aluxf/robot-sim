"""
Robot Simulator Module
------------------------

This module implements a simulation of a toy robot moving on a square tabletop.
The robot can be placed on the table, moved, rotated left or right, and report its
current position. The table is defined by its width and height, and the robot is not
allowed to move off the table.

Classes:
    Direction: Defines the four cardinal directions and provides methods for rotation.
    Environment: Represents the tabletop and provides a method to check valid positions.
    Position: Stores the coordinates of the robot.
    Robot: Implements the robot's behavior, including placement, movement, rotation, and reporting.
    Interface: Provides a command parser and executor to interact with the robot.
"""


class Direction:
    """
    Represents the cardinal directions for the robot's orientation.

    Attributes:
        NORTH (str): Represents the north direction.
        EAST (str): Represents the east direction.
        SOUTH (str): Represents the south direction.
        WEST (str): Represents the west direction.
    """
    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'

    @staticmethod
    def is_valid_direction(direction):
        """
        Check if a given direction is valid.

        Args:
            direction (str): The direction to validate.

        Returns:
            bool: True if the direction is one of NORTH, EAST, SOUTH, or WEST.
        """
        return direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    # TODO: Refactor implementation
    @staticmethod
    def rotate_left(direction):
        """
        Rotate the given direction 90 degrees to the left.

        Args:
            direction (str): The current direction.

        Returns:
            str: The new direction after a left turn.
        """
        if direction == Direction.NORTH:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.SOUTH
        elif direction == Direction.SOUTH:
            return Direction.EAST
        elif direction == Direction.EAST:
            return Direction.NORTH

    @staticmethod
    def rotate_right(direction):
        """
        Rotate the given direction 90 degrees to the right.

        Args:
            direction (str): The current direction.

        Returns:
            str: The new direction after a right turn.
        """
        if direction == Direction.NORTH:
            return Direction.EAST
        elif direction == Direction.EAST:
            return Direction.SOUTH
        elif direction == Direction.SOUTH:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.NORTH


class Environment:
    """
    Represents the simulation environment (the tabletop).

    Attributes:
        width (int): The width of the table.
        height (int): The height of the table.
    """

    def __init__(self, width, height):
        """
        Initialize the environment with given dimensions.

        Args:
            width (int): The width of the tabletop.
            height (int): The height of the tabletop.
        """
        self.width = width
        self.height = height

    def is_valid_position(self, x, y):
        """
        Check if a given (x, y) coordinate is within the environment boundaries.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height


class Position:
    """
    Represents a position on the tabletop.

    Attributes:
        x (int): The x-coordinate.
        y (int): The y-coordinate.
    """

    def __init__(self, x, y):
        """
        Initialize a Position with x and y coordinates.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
        """
        self.x = x
        self.y = y

    def update(self, x, y):
        """
        Update the position to new coordinates.

        Args:
            x (int): New x-coordinate.
            y (int): New y-coordinate.
        """
        self.x = x
        self.y = y


class Robot:
    """
    Implements the robot's functionality, including placing, moving, rotating,
    and reporting its position.

    Attributes:
        position (Position): The current position of the robot.
        f (str): The current facing direction.
        environment (Environment): The environment in which the robot moves.
    """

    def __init__(self, x=0, y=0, f=Direction.NORTH, environment=Environment(5, 5)):
        """
        Initialize the Robot with a starting position, direction, and environment.

        If the provided position is invalid, defaults to (0, 0).

        Args:
            x (int): The starting x-coordinate.
            y (int): The starting y-coordinate.
            f (str): The initial facing direction.
            environment (Environment): The simulation environment.
        """
        self.f = f
        self.environment = environment
        if not self.environment.is_valid_position(x, y):
            x = 0
            y = 0
        self.position = Position(x, y)

    def place(self, x, y, f):
        """
        Place the robot at the specified position and direction if valid.

        Args:
            x (int): The x-coordinate to place the robot.
            y (int): The y-coordinate to place the robot.
            f (str): The facing direction.

        Returns:
            bool: True if placement was successful, False otherwise.
        """
        if Direction.is_valid_direction(f) and self.environment.is_valid_position(x, y):
            self.position = Position(x, y)
            self.f = f
            return True
        return False

    def move(self):
        """
        Move the robot one unit in the direction it is currently facing.

        Returns:
            bool: True if the move is successful, False if the move would
                  cause the robot to leave the environment.
        """
        new_x = self.position.x
        new_y = self.position.y

        if self.f == Direction.NORTH:
            new_y += 1
        elif self.f == Direction.EAST:
            new_x += 1
        elif self.f == Direction.SOUTH:
            new_y -= 1
        elif self.f == Direction.WEST:
            new_x -= 1

        if self.environment.is_valid_position(new_x, new_y):
            self.position.update(new_x, new_y)
            return True
        return False

    def rotate(self, rotation):
        """
        Rotate the robot 90 degrees based on the specified rotation command.

        Args:
            rotation (str): Either "LEFT" or "RIGHT".

        Returns:
            bool: Always returns True after rotation.
        """
        if rotation == "LEFT":
            self.f = Direction.rotate_left(self.f)
        elif rotation == "RIGHT":
            self.f = Direction.rotate_right(self.f)
        return True

    def report(self):
        """
        Report the current position and direction of the robot.

        Returns:
            str: A string representation of the robot's current state.
                 Format: "Report: x,y,DIRECTION"
        """
        report_message = f"Report: {self.position.x},{self.position.y},{self.f}"
        print(report_message)
        return report_message


class Interface:
    """
    Provides an interface for parsing and executing commands on the robot.
    
    Attributes:
        robot (Robot): The robot instance to control.
        commands (dict): A mapping of command strings to their corresponding functions.
        command_history (list): A history of executed commands.
    """

    def __init__(self, robot=Robot(), custom_commands={}):
        """
        Initialize the Interface with a robot and optional custom commands.

        Args:
            robot (Robot): The robot to control.
            custom_commands (dict): A dictionary of additional commands.
        """
        self.robot = robot
        self.commands = custom_commands | {
            "MOVE": self.robot.move,
            "LEFT": lambda: self.robot.rotate("LEFT"),
            "RIGHT": lambda: self.robot.rotate("RIGHT"),
            "REPORT": self.robot.report,
            "PLACE": self.robot.place
        }
        self.command_history = []

    def parse_command(self, input):
        """
        Parse and execute a single command input.

        For the PLACE command, the input must be in the format:
            PLACE,x,y,DIRECTION

        Args:
            input (str): The command string.

        Raises:
            ValueError: If the command is illegal, the arguments are invalid,
                        or the command fails to execute.
        """
        potential_command = input.split(",")[0]

        if self.is_command_prohibited(potential_command):
            raise ValueError(f"Illegal command: {input}")

        # Handle commands with arguments.
        if potential_command == "PLACE":
            try:
                args = input.split(",")[1:]
                if len(args) != 3:
                    raise ValueError(f"Invalid arguments: {input}")
                parsed_args = [int(args[0]), int(args[1]), args[2]]
                command_result = self.commands[potential_command](*parsed_args)
                if not command_result:
                    raise ValueError(f"Invalid arguments: {input}")
                self.command_history.append(potential_command)
                return
            except Exception as e:
                raise ValueError(f"Invalid type of arguments: {input}") from e

        # Handle commands without arguments.
        if potential_command in self.commands:
            result = self.commands[potential_command]()
            if not result:
                raise ValueError(f"Failed to execute: {input}")
            self.command_history.append(potential_command)
            return

        raise ValueError(f"Invalid command: {input}")

    def is_command_prohibited(self, command):
        """
        Determine if a command is prohibited based on command history.

        No commands other than PLACE are allowed until a valid PLACE command
        has been executed.

        Args:
            command (str): The command to check.

        Returns:
            bool: True if the command is prohibited, False otherwise.
        """
        if command != "PLACE" and len(self.command_history) == 0:
            return True
        return False

    def execute(self, command):
        """
        Execute a command and print the command along with any errors.

        Args:
            command (str): The command string to execute.
        """
        print(command)
        try:
            self.parse_command(command)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Create the simulation environment and robot.
    env = Environment(5, 5)
    robot = Robot(environment=env)
    interface = Interface(robot=robot)

    # Read commands from a file and execute them.
    with open('random_commands/commands_1.txt', 'r') as file:
        commands = file.readlines()

    for command in commands:
        command = command.strip()
        if command:
            interface.execute(command)
