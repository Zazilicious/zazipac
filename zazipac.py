import os
import sys
import tty
import termios

# Define constants
EMPTY = ' '
PACMAN = 'C'
DOT = '.'
WALL = '#'

# Game map
map = [
    "#############################",
    "#............##............  #",
    "#.####.#####.##. ##### . ##. #",
    "#.#  #.#   #     #   #.#  #. #",
    "#.#  #.#   ### ###   #.#  #. #",
    "#.####.      P C       ####. #",
    "#............##............. #",
    "#############################",
    "  WSAD to move; q to quit"
]

# Pac-Man's initial position
pacManRow = 5
pacManCol = 12

# Function to display the map
def display_map():
    for row in range(len(map)):
        line = ""
        for col in range(len(map[row])):
            if row == pacManRow and col == pacManCol:
                line += PACMAN
            else:
                line += map[row][col]
        print(line)

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
    global pacManRow, pacManCol
    # Move Pac-Man based on user input
    if key == 'w' and map[pacManRow - 1][pacManCol] != WALL:
        pacManRow -= 1
    elif key == 's' and map[pacManRow + 1][pacManCol] != WALL:
        pacManRow += 1
    elif key == 'a' and map[pacManRow][pacManCol - 1] != WALL:
        pacManCol -= 1
    elif key == 'd' and map[pacManRow][pacManCol + 1] != WALL:
        pacManCol += 1

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to start the game
def start_game():
    display_map()

    while True:
        key = get_user_input()
        if key == 'q':
            break
        handle_input(key)
        clear_console()
        display_map()

# Start the game
start_game()
