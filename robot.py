from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

class Robot:
    def __init__(self, x=0, y=0, f=Direction.NORTH):
        self.x = x
        self.y = y
        self.f = f
    def move(self):
        pass
    def rotate(self, direction):
        if direction == 'LEFT':
            pass
        if direction == 'RIGHT':
            pass
    def report(self):
        pass