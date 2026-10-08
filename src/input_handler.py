
"""
Refactored input_handler.py
Handles user interaction, input parsing, coordinate conversion, and validation.
Returns:
    (row, col, mode): 
        row (int): 0-indexed row (0-9)
        col (int): 0-indexed col (0-9)
        mode (bool): False for Left-click (uncover), True for Right-click (flag)
    (-1, -1, False) on invalid input.
"""

def get_input():
    # Collect cell coordinate
    raw_cell = input("Enter a cell (e.g. A1, J10): ").strip().upper()
    if not raw_cell:
        print("Error: Empty cell input.")
        return (-1, -1, False)

    if len(raw_cell) < 2:
        print("Error: Incomplete coordinate. Expected format like 'A1'.")
        return (-1, -1, False)

    col_letters = "ABCDEFGHIJ"
    col_char = raw_cell[0]
    row_part = raw_cell[1:]

    # Validate column letter
    if col_char not in col_letters:
        print(f"Error: Invalid column '{col_char}'. Must be between A and J.")
        return (-1, -1, False)

    # Validate row digits
    if not row_part.isdigit():
        print(f"Error: '{row_part}' is not a valid row number.")
        return (-1, -1, False)

    row = int(row_part) - 1
    if not (0 <= row <= 9):
        print(f"Error: Row {row + 1} is out of bounds (1-10).")
        return (-1, -1, False)

    col = col_letters.index(col_char)

    # Collect click action mode
    click_mode = input("Enter L (uncover / left click) or R (flag / right click): ").strip().upper()
    if click_mode not in ("L", "R"):
        print("Error: Invalid click mode. Please enter 'L' or 'R'.")
        return (-1, -1, False)

    # False = Left click (uncover), True = Right click (flag)
    is_flag = (click_mode == "R")

    return (row, col, is_flag)
