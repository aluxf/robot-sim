# Robot Simulator

This project implements a simulation of a toy robot moving on a square tabletop. The robot can be placed on the table, moved, rotated left or right, and report its current position. The table is defined by its width and height, and the robot is not allowed to move off the table.

## Project Structure

- `robot.py`: Contains the main implementation of the robot simulator.
- `generate_commands.py`: Script to generate random command files for manual testing.
- `test.py`: Contains unit tests for the robot simulator.
- `random_commands/`: Directory containing randomly generated command files.
- `robot_tests/`: Directory containing predefined test cases.

## Pre-requisites

- Python 3.11.6 or higher

## Usage

### Running the Simulator

To run the simulator with a predefined command file:

```sh
python robot.py 'path/to/command_file.txt'

```
### Generating Random Command Files

```sh
python generate_commands.py
```

### Running Tests

```sh
python test.py
```

### Adding new file tests

In `robot_tests/`, create a input file `filename_input.txt` and expected output file `filename_expected.txt`.

The input file should end with command `REPORT` and expected output file should contain the expected output of the command.


### Custom Example

```py

from robot import Environment, Robot, Interface

# Create the simulation environment and robot.
env = Environment(5, 5)
robot = Robot(environment=env)
interface = Interface(robot=robot)

# Read commands from a file and execute them.
with open('path/to/command_file.txt', 'r') as file:
    commands = file.readlines()

for command in commands:
    command = command.strip()
    if command:
        interface.execute(command)
```