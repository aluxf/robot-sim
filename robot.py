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
        report_message = f"Report: {self.position.x},{self.position.y},{self.f}"
        print(report_message)
        return report_message


class Interface:

    def __init__(self, robot=Robot(), commands={} ):
        self.robot = robot
        self.commands = {
            "MOVE": self.robot.move,
            "LEFT": lambda: self.robot.rotate("LEFT"),
            "RIGHT": lambda: self.robot.rotate("RIGHT"),
            "REPORT": self.robot.report,
            "PLACE": self.robot.place
        }
        self.command_history = []
    
    def parse_command(self, input):
        potential_command = input.split(",")[0]

        if self.is_command_prohibited(potential_command):
            raise ValueError(f"Illegal command: {input}")

        if potential_command == "PLACE":
            try:
                args = input.split(",")[1:]
                if len(args) != 3:
                    raise ValueError(f"Invalid arguments: {input}")
                parsed_args = [int(args[0]), int(args[1]), args[2]]
                self.command_history.append(potential_command)
                return self.commands[potential_command](*parsed_args)
            except Exception as e:
                print(f"Error: {e}")
                raise ValueError(f"Invalid type of arguments: {input}")
                
        # Non-argument commands
        if potential_command in self.commands:
            self.command_history.append(potential_command)
            print(potential_command)
            return self.commands[potential_command]()
        
        raise ValueError(f"Invalid command: {input}")
    
    def is_command_prohibited(self, command):
        if command != "PLACE" and len(self.command_history) == 0:
            return True
        return False

    def execute(self, command):
        try:
            self.parse_command(command)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interface = Interface()
    interface.execute("MOVE")
    interface.execute("PLACE,1,1,NORTH")
    interface.execute("REPORT")
    interface.execute("LEFT")
    interface.execute("MOVE")
    interface.execute("REPORT")
    interface.execute("MOVE")
    interface.execute("REPORT")

    
