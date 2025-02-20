class Direction:
    NORTH = 'NORTH'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    WEST = 'WEST'

    # TODO: Refactor implementation
    @staticmethod
    def rotate_left(direction):
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
        if direction == Direction.NORTH:
            return Direction.EAST
        elif direction == Direction.EAST:
            return Direction.SOUTH
        elif direction == Direction.SOUTH:
            return Direction.WEST
        elif direction == Direction.WEST:
            return Direction.NORTH

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self, x, y):
        self.x = x
        self.y = y
        


class Robot:
    def __init__(self, x=0, y=0, f=Direction.NORTH, environment=Environment(5, 5)):
        self.f = f
        self.environment = environment
        if not self.environment.is_valid_position(x, y):
            x = 0
            y = 0
        self.position = Position(x, y)
    def place(self, x, y, f):
        if self.environment.is_valid_position(x, y):
            self.position = Position(x, y)
            self.f = f
            return True
        return False
        
    def move(self):
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
        
        if(self.environment.is_valid_position(new_x, new_y)):
            self.position.update(new_x, new_y)
            return True
        return False

    def rotate(self, rotation):
        if rotation == "LEFT":
            self.f = Direction.rotate_left(self.f)
        elif rotation == "RIGHT":
            self.f = Direction.rotate_right(self.f)
    def report(self):
        print(f"Report: {self.position.x},{self.position.y},{self.f}")


class Interface:

    def __init__(self):
        self.robot = Robot()
        self.single_commands = {
            "MOVE": self.robot.move,
            "LEFT": self.robot.rotate("LEFT"),
            "RIGHT": self.robot.rotate("RIGHT"),
            "REPORT": self.robot.report
        }
        self.argument_commands = {
            "PLACE": self.robot.place
        }
    
    def parse_input(self, input):
        pass
    
    def execute(self, command):
        pass
