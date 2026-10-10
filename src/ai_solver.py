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
        hidden_states = (0, 3)
        flagged_states = (1, 4)

        # Apply the flagging rule before considering any cells to uncover.
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) != 2: #Skips cells already uncovered are marked safe 
                    continue

                neighbors = []
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if board.in_bounds(nr, nc):
                            neighbors.append((nr, nc))

                hidden_neighbors = [
                    (nr, nc) for nr, nc in neighbors
                    if board.getCellState(nr, nc) in hidden_states
                ]
                clue = board.numBombNeighbors(row, col)

                if hidden_neighbors and len(hidden_neighbors) == clue:
                    for nr, nc in hidden_neighbors:
                        board.setState(nr, nc, True)
                        column_letter = chr(ord("A") + nc)
                        print(f"AI flagged cell [{column_letter}{nr + 1}]")
                    return

        # If flagging is not possible, uncover neighbors when all mines are flagged.
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) != 2:
                    continue

                hidden_neighbors = []
                flagged_count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if not board.in_bounds(nr, nc):
                            continue

                        state = board.getCellState(nr, nc)
                        if state in hidden_states:
                            hidden_neighbors.append((nr, nc))
                        elif state in flagged_states:
                            flagged_count += 1

                clue = board.numBombNeighbors(row, col)
                if hidden_neighbors and flagged_count == clue:
                    for nr, nc in hidden_neighbors:
                        board.setState(nr, nc, False)
                        column_letter = chr(ord("A") + nc)
                        print(f"AI uncovered cell [{column_letter}{nr + 1}]")
                    return

        # Neither rule applies: choose a random hidden cell and uncover it.
        possible_cells = []
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) in hidden_states:
                    possible_cells.append((row, col))

        if possible_cells:
            row, col = random.choice(possible_cells)
            board.setState(row, col, False)
            column_letter = chr(ord("A") + col)
            print(f"AI uncovered cell [{column_letter}{row + 1}]")

    elif difficulty == "hard":
        #TODO Hard difficulty
        pass