import random
import os

# Generate command files for 4x4 environment

def generate_place_command():
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    direction = random.choice(["NORTH", "EAST", "SOUTH", "WEST"])
    return f"PLACE,{x},{y},{direction}"

def generate_command_file(filename, num_commands, place_first):
    commands = ["PLACE", "MOVE", "MOVE", "LEFT", "RIGHT"]
    invalid_commands = ["JUMP", "PLACE,1,2,3", "PLACE,1,2", "PLACE,1,2,NORTH,EXTRA", "PLACE,999,999,NORTH"]

    with open(filename, 'w') as file:
        if place_first:
            file.write(generate_place_command() + "\n")
            file.write("REPORT\n")
        
        for _ in range(num_commands):
            # 10% chance to use an invalid command
            if random.random() < 0.1:  
                command = random.choice(invalid_commands)
            else:
                command = random.choice(commands)
                if command == "PLACE":
                    command = generate_place_command()
            
            file.write(f"{command}\n")

            # REPORT after every command
            file.write("REPORT\n")

def generate_command_files(num_files, num_commands_per_file, place_first):
    for i in range(num_files):
        filename = f"commands/commands_{i+1}.txt"
        generate_command_file(filename, num_commands_per_file, place_first)
        print(f"Generated {filename}")

if __name__ == "__main__":
    os.makedirs("commands", exist_ok=True)
    files = 10
    commands_per_file = 20
    place_first = True


    generate_command_files(files, commands_per_file, place_first)