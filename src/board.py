"""
board.py
Manages the board state, mine population, neighbor calculations, and win/loss states.
"""
import random

class Board:
    def __init__(self, numMinesInput: int = 10, rows: int = 10, cols: int = 10):
        self.__rows = rows
        self.__cols = cols
        self.__numMines = numMinesInput

        # Cell States:
        # 0 = Unchecked safe spot
        # 1 = Flagged safe spot (false flag)
        # 2 = Checked/uncovered safe spot
        # 3 = Unchecked mine
        # 4 = Flagged mine
        self.__board = [[0 for _ in range(self.__cols)] for _ in range(self.__rows)]
        self.__gameState = 0  # 0: In progress, -1: Loss, 1: Win
        self.__remainingFlags = numMinesInput

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.__rows and 0 <= col < self.__cols

    def populateBoard(self, clickedCellRow: int, clickedCellCol: int):
        """Randomly place mines ensuring the first clicked tile is safe."""
        mines_placed = 0
        while mines_placed < self.getNumMines():
            r = random.randint(0, self.getRows() - 1)
            c = random.randint(0, self.getCols() - 1)
            if (r == clickedCellRow and c == clickedCellCol) or self.getCellState(r, c) == 3:
                continue
            self.__board[r][c] = 3
            mines_placed += 1

    def setState(self, clickedCellRow: int, clickedCellCol: int, isFlagging: bool = False):
        """
        Updates cell state:
        - If isFlagging is True: toggles flag between 0 <-> 1 and 3 <-> 4.
        - If isFlagging is False: uncovers safe cells (0) or triggers loss on mine (3).
        """
        if not self.in_bounds(clickedCellRow, clickedCellCol):
            return

        current_state = self.getCellState(clickedCellRow, clickedCellCol)

        if isFlagging:
            if current_state == 3:
                self.__board[clickedCellRow][clickedCellCol] = 4
                self.__remainingFlags -= 1
            elif current_state == 4:
                self.__board[clickedCellRow][clickedCellCol] = 3
                self.__remainingFlags += 1
            elif current_state == 0:
                self.__board[clickedCellRow][clickedCellCol] = 1
                self.__remainingFlags -= 1
            elif current_state == 1:
                self.__board[clickedCellRow][clickedCellCol] = 0
                self.__remainingFlags += 1
            return

        # Left-click (uncover)
        if current_state == 3:
            self.__gameState = -1
            return

        if current_state == 0:
            self.__board[clickedCellRow][clickedCellCol] = 2

            # Cascade reveal if no adjacent mines
            if self.numBombNeighbors(clickedCellRow, clickedCellCol) == 0:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = clickedCellRow + dr, clickedCellCol + dc
                        if self.in_bounds(nr, nc) and self.getCellState(nr, nc) == 0:
                            self.setState(nr, nc, isFlagging=False)

    def numBombNeighbors(self, row: int, col: int) -> int:
        """Returns the number of mines adjacent to (row, col)."""
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.in_bounds(nr, nc):
                    state = self.getCellState(nr, nc)
                    if state in (3, 4):
                        count += 1
        return count

    def hasWon(self) -> int:
        """
        Returns:
         -1: Lost
          1: Won
          0: In progress
        """
        if self.__gameState == -1:
            return -1

        for r in range(self.getRows()):
            for c in range(self.getCols()):
                state = self.getCellState(r, c)
                if state in (0, 1):
                    self.__gameState = 0
                    return 0

        self.__gameState = 1
        return 1

    def getRows(self) -> int:
        return self.__rows

    def getCols(self) -> int:
        return self.__cols

    def getCellState(self, row: int, col: int) -> int:
        return self.__board[row][col]

    def getNumRemainingFlags(self) -> int:
        return self.__remainingFlags

    def remaining_mines(self) -> int:
        """Alias for getNumRemainingFlags."""
        return self.getNumRemainingFlags()

    def getNumMines(self) -> int:
        return self.__numMines
