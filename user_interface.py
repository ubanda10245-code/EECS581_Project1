"""
Refactored user_interface.py
Handles outputting the board state to the terminal.
"""
from board import Board

class User_Interface:
    def __init__(self, i_Board: Board):
        self.myBoard = i_Board 
        self.rows = self.myBoard.getRows()
        self.cols = self.myBoard.getCols()

    def print_board(self, loss=False):
        # Display remaining flag count
        print(f"   Remaining Flags: {self.myBoard.getNumRemainingFlags()}")

        # Dynamically generate column headers (A, B, C...)
        col_labels = [chr(ord('A') + i) for i in range(self.cols)]
        print("    " + " ".join(col_labels))
        print("   +" + "--" * self.cols + "-+")

        for row in range(self.rows):
            # Format row numbers with 2-digit padding
            row_str = f"{row + 1:2} | "

            for col in range(self.cols):
                state = self.myBoard.getCellState(row, col)

                if state == 2:  # Checked / uncovered spot
                    neighbor_mines = self.myBoard.numBombNeighbors(row, col)
                    cell_char = str(neighbor_mines) if neighbor_mines != 0 else " "
                elif not loss:  # Active gameplay
                    if state in (0, 3):    # Unchecked spot (safe or mine)
                        cell_char = "X"
                    elif state in (1, 4):  # Flagged spot (safe or mine)
                        cell_char = "F"
                    else:
                        cell_char = "?"
                else:  # Loss display
                    if state == 0:         # Unchecked safe spot
                        cell_char = "X"
                    elif state == 3:       # Unchecked mine
                        cell_char = "M"
                    elif state == 4:       # Correctly flagged mine
                        cell_char = "F"
                    elif state == 1:       # Incorrectly flagged safe spot (false flag)
                        cell_char = "/"
                    else:
                        cell_char = "?"

                row_str += cell_char + " "

            row_str += "|"
            print(row_str)

        print("   +" + "--" * self.cols + "-+")
