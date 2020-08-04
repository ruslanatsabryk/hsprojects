# Read the input
def get_field(field_input="_________"):
    for i in range(3):
        row = field_input[0:3]
        field.append(list(row))
        field_input = field_input[3:]

# Filling the field
def print_field():
    print("-" * 9)
    for row in field:
        print("|", end="", sep="")
        for col in row:
            print(f" {col}", end="")
        print(" |")
    print("-" * 9)

def check_game_state():
    # Check impossible state and count empty cells
    x, o, empty = 0, 0, 0
    for row in range(3):
        for col in range(3):
            x += 1 if field[row][col] == 'X' else 0
            o += 1 if field[row][col] == 'O' else 0
            empty += 1 if field[row][col] == '_' else 0
    impossible = True if abs(x - o) > 1 else False
    # main and secondary diagonal check for winner
    diag0 = [field[ind][ind] for ind in range(3)]
    diag1 = [field[2 - ind][ind] for ind in range(3)]
    x_win = True if "".join(diag0) == "XXX" or "".join(diag1) == "XXX" else False
    o_win = True if "".join(diag0) == "OOO" or "".join(diag1) == "OOO" else False
    # columns and rows check for winner
    for ind in range(3):
        next_col = [field[row][ind] for row in range(3)]
        next_row = field[ind]
        x_win = True if "".join(next_row) == "XXX" or "".join(next_col) == "XXX" else x_win
        o_win = True if "".join(next_row) == "OOO" or "".join(next_col) == "OOO" else o_win
    draw = True if empty == 0 and not x_win and not o_win else False
    state = "Impossible" if impossible or (x_win and o_win) else "Draw" if draw else \
            "X wins" if x_win else "O wins" if o_win else "Game not finished"
    return state

def convert_coordinates(a, b):
    # Convert coordinates to Python rules compliant
    transform_table = [[[2, 0], [1, 0], [0, 0]],
                       [[2, 1], [1, 1], [0, 1]],
                       [[2, 2], [1, 2], [0, 2]]]
    row, col = transform_table[a - 1][b - 1]
    return row, col

# Start the game
field = []
get_field()
print_field()
game_state = check_game_state()
x_move = True
while game_state == "Game not finished":
    coord = input("Enter the coordinates")
    # check coordinates
    ab = coord.split(" ")
    if len(ab) != 2 or not ab[0].isdigit() or not ab[1].isdigit():
        print("You should enter numbers")
        continue
    if int(ab[0]) not in [1, 2, 3] or int(ab[1]) not in [1, 2, 3]:
        print("Coordinates should be from 1 to 3")
        continue
    x_row, y_col = convert_coordinates(int(ab[0]), int(ab[1]))
    if field[x_row][y_col] != "_":
        print("This cell is occupied! Choose another one!")
        continue
    # Transfer the move to the field, change player
    field[x_row][y_col] = "X" if x_move else "O"
    print_field()
    x_move = not x_move
    game_state = check_game_state()
    if game_state in ["X wins", "O wins", "Draw"]:
        print(game_state)
