import time
import os
import random
import sys

#creates a random list of 1s and 0s to use as cells on the grid
#1 = live cells, 0 = dead cells
def create_initial_grid(rows, cols):

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            #Randomize addition of dead and alive cells to the grid
            if random.randint(0, 7) == 0:
                grid_rows += [1]
            else:
                grid_rows += [0]
        grid += [grid_rows]
    return grid

def print_grid(rows, cols, grid, generation):

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    else:
        print("OS Error. Please open a github issue.\n\r")

    # Compile the output string together and then print it to console
    output_str = ""
    output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            else:
                output_str += "O "
        output_str += "\n\r"
    print(output_str, end=" ")

#Recreates grid using the rules of the game
def create_next_grid(rows, cols, grid, next_grid):

    for row in range(rows):
        for col in range(cols):
            # Get the number of live cells adjacent to the cell at grid[row][col]
            live_neighbors = get_live_neighbors(row, col, rows, cols, grid)

            # If the number of surrounding live cells is < 2 or > 3 then we make the cell at grid[row][col] a dead cell
            if live_neighbors < 2 or live_neighbors > 3:
                next_grid[row][col] = 0
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] was previously dead then make
            # the cell into a live cell
            elif live_neighbors == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] is alive keep it alive
            else:
                next_grid[row][col] = grid[row][col]

#checks number of living neightbord
def get_live_neighbors(row, col, rows, cols, grid):
    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Make sure to count the center cell located at grid[row][col]
            if not (i == 0 and j == 0):
                # Using the modulo operator (%) the grid wraps around
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]
    return life_sum

#check if grid changes per generation
def grid_changing(rows, cols, grid, next_grid):
    
    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False

#function to get integers for grid size
def get_integer_value(prompt, low, high):

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Input was not a valid integer value.")
            continue
        if value < low or value > high:
            print("Input was not inside the bounds (value <= {0} or value >= {1}).".format(low, high))
        else:
            break
    return value

#function to resize terminal 
def resize_terminal(rows, cols):
    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    else:
        print("Terminal Resize Failed. Please open a github issue.\n\r")

#setup terminal and run GameOfLife!
def run_game():

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    else:
        print("OS Error. Please open a github issue.\n\r")

    # Get the number of rows and columns for the Game of Life grid
    rows = get_integer_value("Enter the number of rows (10-60): ", 10, 60)
    
    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    else:
        print("OS Error. Please open a github issue.\n\r")
    
    cols = get_integer_value("Enter the number of cols (10-118): ", 10, 118)

    # Get the number of generations that the Game of Life should run for
    generations = 5000
    resize_terminal(rows, cols)

    # Create the initial random Game of Life grids
    current_generation = create_initial_grid(rows, cols)
    next_generation = create_initial_grid(rows, cols)

    # Run Game of Life sequence
    gen = 1
    for gen in range(1, generations + 1):
        if not grid_changing(rows, cols, current_generation, next_generation):
            break
        print_grid(rows, cols, current_generation, gen)
        create_next_grid(rows, cols, current_generation, next_generation)
        time.sleep(1 / 5.0)
        current_generation, next_generation = next_generation, current_generation

    print_grid(rows, cols, current_generation, gen)
    return input("<Enter> to exit or r to run again: ")


# Start the Game of Life
run = "r"
while run == "r":
    out = run_game()
    run = out