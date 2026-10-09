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

        # Added 10/9 Niles C: Ask the player to choose a game mode.
        while True:
            gameMode = input("Choose game mode: Solo, Multiplayer, or AI: ").strip().lower()
            if gameMode in ("solo", "multiplayer", "ai"):
                break
            print("Invalid game mode. Enter Solo, Multiplayer, or AI.")

        # Added 10/9 Niles C: Store AI difficulty for the next team member to use.
        aiDifficulty = None
        if gameMode == "ai":
            while True:
                aiDifficulty = input("Choose AI difficulty: Easy, Medium, or Hard: ").strip().lower()
                if aiDifficulty in ("easy", "medium", "hard"):
                    break
                print("Invalid difficulty. Enter Easy, Medium, or Hard.")

        # Added 10/9 Niles C: Initialize the multiplayer player variable.
        if gameMode == "multiplayer":
            currentPlayer = 1

        myBoard = Board(mines)
        ui = User_Interface(myBoard)
        print("Start playing\n")
        ui.print_board()

        currentPlayer = 1

        # First move: Only allow left-click / uncover
        while True:
            row, col, is_flag = get_input(currentPlayer)
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

        currentPlayer = 2


        ai_solver(myBoard, "easy")

        ui.print_board()

        # Active gameplay loop
        while myBoard.hasWon() == 0:
            print("Status: Playing")

            while True:
                row, col, is_flag = get_input(currentPlayer)
                if row != -1:
                    break
                print("Invalid input, try again.")

            myBoard.setState(row, col, is_flag)

            # Switch players after a valid move
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1
            
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
