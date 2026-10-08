import random

def ai_solver(board, difficulty):
    if difficulty == "easy":
        possible_cells = []

        # Find all cells the AI is allowed to uncover
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                state = board.getCellState(row, col)

                # 0 = unchecked safe cell
                # 3 = unchecked mine
                if state == 0 or state == 3:
                    possible_cells.append((row, col))

        # Randomly choose one possible cell
        if possible_cells:
            row, col = random.choice(possible_cells)

            # Uncover the selected cell
            board.setState(row, col, False)

            # Convert column number to a letter
            column_letter = chr(ord('A') + col)

            print(f"AI uncovered cell [{column_letter}{row + 1}]")

    elif difficulty == "medium":
        #TODO Medium difficulty
        pass

    elif difficulty == "hard":
        #TODO Hard difficulty
        pass