import os
import sys
import tty
import termios
import random
import time

# Define constants
EMPTY = ' '
ZaziPac = 'C'
DOT = '.'
WALL = '#'
GHOST = 'A'

# Game map (with walls, dots, and more empty space for movement)
game_map = [
    "#############################",
    "#...........................#",
    "#.####   .#. #. ##### . ## .#",
    "#.#  #.              #.# . .#",
    "#.#   .#    ## ##    #. . #.#",
    "#.### .              ####.  #",
    "#.............#.............#",
    "#############################",
    "  WSAD to move; q to quit"
]

# ZaziPac's initial position
ZaziPacRow = 5
ZaziPacCol = 12

# Ghost's initial position
ghostRow = 5
ghostCol = 8

# Score and Dot count
score = 0
total_dots = sum(row.count(DOT) for row in game_map)

# Function to display the map
def display_map():
    for row in range(len(game_map)):
        line = ""
        for col in range(len(game_map[row])):
            if row == ZaziPacRow and col == ZaziPacCol:
                line += ZaziPac
            elif row == ghostRow and col == ghostCol:
                line += GHOST
            else:
                line += game_map[row][col]
        print(line)
    print(f"Score: {score}  Dots Remaining: {total_dots}")

# Function to get user input
def get_user_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key.lower()

# Function to handle user input
def handle_input(key):
    global ZaziPacRow, ZaziPacCol
    # Move ZaziPac based on user input
    if key == 'w' and game_map[ZaziPacRow - 1][ZaziPacCol] != WALL:
        ZaziPacRow -= 1
    elif key == 's' and game_map[ZaziPacRow + 1][ZaziPacCol] != WALL:
        ZaziPacRow += 1
    elif key == 'a' and game_map[ZaziPacRow][ZaziPacCol - 1] != WALL:
        ZaziPacCol -= 1
    elif key == 'd' and game_map[ZaziPacRow][ZaziPacCol + 1] != WALL:
        ZaziPacCol += 1

    # Check if ZaziPac eats a dot
    if game_map[ZaziPacRow][ZaziPacCol] == DOT:
        global score, total_dots
        score += 10  # Increase score
        total_dots -= 1  # Decrease remaining dots
        game_map[ZaziPacRow] = game_map[ZaziPacRow][:ZaziPacCol] + EMPTY + game_map[ZaziPacRow][ZaziPacCol+1:]  # Remove the dot

# Function to move the ghost to chase ZaziPac
def ghost_behave():
    global ghostRow, ghostCol
    # Determine the direction of movement based on ZaziPac's position
    if ZaziPacRow < ghostRow and game_map[ghostRow - 1][ghostCol] != WALL:
        ghostRow -= 1  # Move up
    elif ZaziPacRow > ghostRow and game_map[ghostRow + 1][ghostCol] != WALL:
        ghostRow += 1  # Move down
    elif ZaziPacCol < ghostCol and game_map[ghostRow][ghostCol - 1] != WALL:
        ghostCol -= 1  # Move left
    elif ZaziPacCol > ghostCol and game_map[ghostRow][ghostCol + 1] != WALL:
        ghostCol += 1  # Move right

# Function to check for collision with ghost
def check_collision():
    if ZaziPacRow == ghostRow and ZaziPacCol == ghostCol:
        print("Game Over! ZaziPac was eaten by a ghost!")
        return True
    return False

# Function to check for win condition
def check_win():
    if total_dots == 0:
        print(f"Congratulations! You win with a score of {score}!")
        return True
    return False

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to start the game
def start_game():
    display_map()

    while True:
        key = get_user_input()
        if key == 'q':
            print("Quitting the game.")
            break
        handle_input(key)
        ghost_behave()

        if check_collision():
            break
        if check_win():
            break

        clear_console()
        display_map()
        time.sleep(0.2)  # Delay to slow down the game loop for better readability

# Start the game
start_game()
