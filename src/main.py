"""
main.py
Implements the main game loop, user flow, and win/loss resolution.
"""
import sys
from pathlib import Path

# Ensures modules in the same directory are found when executed from any path
sys.path.append(str(Path(__file__).resolve().parent))

from board import Board
from input_handler import get_input
from user_interface import User_Interface
from ai_solver import ai_solver

def main():
    while True:
        print("\n=== Welcome to Minesweeper ===")
        uInput = input("Enter Number of Mines [10, 20] or 'QUIT' to quit: ").strip()
        if uInput.upper() == "QUIT":
            break

        try:
            mines = int(uInput)
            if not (10 <= mines <= 20):
                raise ValueError
        except ValueError:
            print("Not a valid integer value for mines. Please enter a number between 10 and 20.")
            continue

        myBoard = Board(mines)
        ui = User_Interface(myBoard)
        print("Start playing\n")
        ui.print_board()

        # First move: Only allow left-click / uncover
        while True:
            row, col, is_flag = get_input()
            if row == -1:
                print("Invalid Cell, Try Again")
                continue
            if is_flag:
                print("Only a left click is allowed for your first move. Try again.")
                continue
            break

        # Populate board avoiding first click, then reveal that cell
        myBoard.populateBoard(row, col)
        myBoard.setState(row, col, False)


        ai_solver(myBoard, "easy")

        ui.print_board()

        # Active gameplay loop
        while myBoard.hasWon() == 0:
            print("Status: Playing")

            while True:
                row, col, is_flag = get_input()
                if row != -1:
                    break
                print("Invalid input, try again.")

            myBoard.setState(row, col, is_flag)


            # AI's move
            ai_solver(myBoard, "easy")
            
            # Display updated board if still playing
            if myBoard.hasWon() == 0:
                ui.print_board()

        # Game conclusion
        result = myBoard.hasWon()
        if result == -1:
            ui.print_board(loss=True)
            print("Status: Game Over: Loss")
            print("Game Over: You Lost.\nTry again?\n")
        elif result == 1:
            ui.print_board(loss=False)
            print("Status: Victory")
            print("You Win! Play Again?\n")
        else:
            raise ValueError(f"An unexpected error occurred (hasWon returned {result})")

    print("Thanks for Playing")

if __name__ == "__main__":
    main()
