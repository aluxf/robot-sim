from dataclasses import dataclass
from enum import Enum

class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

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
        self.position = Position(x, y)
        self.f = f
        self.environment = environment
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
        pass