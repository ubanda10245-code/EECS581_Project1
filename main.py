#main.py
"""
Author: Phoenix Brehm created 9/12/26
Last updated: 9/15/26 - by Phoenix Brehm
Code is authored by Phoenix Brehm
The goal of the main.py is to implement the game logic and game loop
Functions implemented are:
    main which takes in no input and returns none
This file loops and plays the game checking if the player has won or lost and sends inputs to the board to update the state of cells.
"""
from board import Board
from input_handler import get_input
from user_interface import User_Interface
from ai_solver import ai_solver
def main():
    #game loop
    while(True):
        print("Welcome to Minesweeper!")
        uInput = input("Enter Number of Mines [10, 20] or 'QUIT' to quit: ")
        if(uInput == "QUIT"):
            break
        try:
            mines = int(uInput) #try casting user input to int, if not int raise error
            if(mines >= 10 and mines <= 20):
                myBoard = Board(mines) #create board
                ui = User_Interface(myBoard) #create ui handler
                print("Start playing")
            else:
                raise ValueError #intended value error for when user inputs values less than 10 or greater than 20
        except: #if mines is not an int or not an int between 10 and 20
            print("Not a valid integer value for mines")
            continue

    
        ui.print_board()
        #wait for user to input on a cell (only allow left click, no flag for first click)
        while True:
            inputSelect = get_input()
            if inputSelect[0] == -1: #checks if invalid cell, if not try again
                print("Invalid Cell, Try Again")
                continue
            if inputSelect[2]: #checks if valid mode (l for first click only)
                print("Only a left click is allowed for your first move Try again")
                continue
            break
        # myBoard.populateBoard(inputSelect[0], inputSelect[1]) #populate board
        # myBoard.setState(inputSelect[0], inputSelect[1]) #clear first click
        # ui.print_board()
        # print("Status: Playing")
        myBoard.populateBoard(inputSelect[0], inputSelect[1])
        myBoard.setState(inputSelect[0], inputSelect[1])

        # Let AI move after the player's first move
        if myBoard.hasWon() == 0:
            ai_solver(myBoard, "easy")

        ui.print_board()

        if myBoard.hasWon() == 0:
            print("Status: Playing")


        while(myBoard.hasWon() == 0): #if player has not won or lost
            #wait for user to input on a cell
            while True:
                inputSelect = get_input()
                if inputSelect[0] != -1:
                    break

            #print board (can be done hopefully painlessly with numBombNeighbors in board class)
            myBoard.setState(inputSelect[0], inputSelect[1], inputSelect[2])
            
            # AI's move
            ai_solver(myBoard, "easy")
            
            # check if the AI ended the game
            if myBoard.hasWon() != 0:
                break
            
            # game is still going
            ui.print_board()
            print("status: playing")


        result = myBoard.hasWon() #store win result
        if(result == -1):
            ui.print_board(True) #print board with hasLost = true displaying mines and false flags
            print("Game Over: You Lost.\nTry again?\n")
            #print board (can be done hopefully painlessly with numBombNeighbors in board class)
            #but this time display all mines and false flags, but keep covered spaces properly covered, likely done with getCellState in board class
        elif(result == 1):
            print("You Win! Play Again?\n")
        else: #should never be reached
            raise ValueError("An unexpected error occurred (hasWon returned {result})")
    print("Thanks for Playing")

main()