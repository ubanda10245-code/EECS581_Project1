import random

def find_121_pattern(board):
    """
    Function: find_121_pattern
    Description: Detect a logically valid 1-2-1 pattern horizontally
                 or vertically and return the cells to flag and uncover.
    Inputs: board, the current Minesweeper board.
    Outputs: A tuple (mines, safe_cells), or None if no valid pattern exists.
    Sources: Original implementation for EECS 581 Project 2.
    Author: Umair Chaudhry
    Creation date: 10/10/2026
    """

    hidden_states = (0, 3)
    flagged_states = (1, 4)

    rows = board.getRows()
    cols = board.getCols()

    # Check horizontal and vertical arrangements.
    for dr, dc in ((0, 1), (1, 0)):
        for row in range(rows):
            for col in range(cols):

                # The three revealed clues must form 1-2-1.
                clues = [
                    (row, col),
                    (row + dr, col + dc),
                    (row + 2 * dr, col + 2 * dc)
                ]

                if not all(
                    board.in_bounds(r, c)
                    and board.getCellState(r, c) == 2
                    for r, c in clues
                ):
                    continue

                clue_values = [
                    board.numBombNeighbors(r, c)
                    for r, c in clues
                ]

                if clue_values != [1, 2, 1]:
                    continue

                # Try the hidden line on either side of the clues.
                for side in (-1, 1):
                    targets = [
                        (r + side * dc, c - side * dr)
                        for r, c in clues
                    ]

                    # All three target cells must be hidden and unflagged.
                    if not all(
                        board.in_bounds(r, c)
                        and board.getCellState(r, c) in hidden_states
                        for r, c in targets
                    ):
                        continue

                    pattern_valid = True

                    # Each clue must have no other hidden neighbors.
                    # Existing flags are accounted for in the clue count.
                    for index, (r, c) in enumerate(clues):
                        hidden_neighbors = set()
                        flagged_count = 0

                        for nr in range(r - 1, r + 2):
                            for nc in range(c - 1, c + 2):
                                if (nr, nc) == (r, c):
                                    continue

                                if not board.in_bounds(nr, nc):
                                    continue

                                state = board.getCellState(nr, nc)

                                if state in hidden_states:
                                    hidden_neighbors.add((nr, nc))
                                elif state in flagged_states:
                                    flagged_count += 1

                        # Only the target cells adjacent to this clue
                        # may remain hidden.
                        expected_hidden = {
                            target for target in targets
                            if max(
                                abs(target[0] - r),
                                abs(target[1] - c)
                            ) == 1
                        }

                        if hidden_neighbors != expected_hidden:
                            pattern_valid = False
                            break

                        remaining_mines = (
                            clue_values[index] - flagged_count
                        )

                        expected_mines = [1, 2, 1][index]

                        if remaining_mines != expected_mines:
                            pattern_valid = False
                            break

                    if pattern_valid:
                        # The two outer cells are mines.
                        # The middle cell is safe.
                        mines = [targets[0], targets[2]]
                        safe_cells = [targets[1]]

                        return mines, safe_cells

    return None

def ai_solver(board, difficulty):
    if difficulty == "easy":
        """ Uncover a random cell, avoiding uncovered and flagged cells.
        """
  
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
        """ Flag cells when the number of hidden neighbors equals the clue's remaining mine count.
            Uncover cells if the number of flagged neighbors equals the clue's mine count.
            Clue is the number of mines adjacent to a revealed cell.
        """
        hidden_states = (0, 3)
        flagged_states = (1, 4)

        # Apply the flagging rule before considering any cells to uncover.
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) != 2: #Skips cells already uncovered
                    continue

                neighbors = [] # Gather all neighboring cells
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if board.in_bounds(nr, nc):
                            neighbors.append((nr, nc))

                hidden_neighbors = []
                flagged_count = 0
                for nr, nc in neighbors:
                    state = board.getCellState(nr, nc)
                    if state in hidden_states: 
                        hidden_neighbors.append((nr, nc))
                    elif state in flagged_states:
                        flagged_count += 1

                clue = board.numBombNeighbors(row, col)

                # If the number of hidden neighbors equals the clue minus the flagged count, flag all hidden neighbors.
                if hidden_neighbors and len(hidden_neighbors) == clue - flagged_count: 
                    for nr, nc in hidden_neighbors:
                        board.setState(nr, nc, True) # Flag the cell
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
                        # skip out-of-bounds neighbors
                        if not board.in_bounds(nr, nc):
                            continue

                        state = board.getCellState(nr, nc)
                        if state in hidden_states:
                            hidden_neighbors.append((nr, nc))
                        elif state in flagged_states:
                            flagged_count += 1

                clue = board.numBombNeighbors(row, col)

                # If the number of flagged neighbors equals the clue, uncover all hidden neighbors.
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
        """ 
        """
        hidden_states = (0, 3)
        flagged_states = (1, 4)

        # Rule 1: Flag hidden neighbors when their count
        # equals the revealed clue's remaining mine count.
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) != 2:
                    continue

                neighbors = []
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue

                        nr, nc = row + dr, col + dc
                        if board.in_bounds(nr, nc):
                            neighbors.append((nr, nc))

                hidden = [
                    (nr, nc) for nr, nc in neighbors
                    if board.getCellState(nr, nc) in hidden_states
                ]

                flagged_count = sum(
                    board.getCellState(nr, nc) in flagged_states
                    for nr, nc in neighbors
                )

                clue = board.numBombNeighbors(row, col)

                if hidden and len(hidden) + flagged_count == clue:
                    for nr, nc in hidden:
                        board.setState(nr, nc, True)
                        letter = chr(ord("A") + nc)
                        print(f"AI flagged cell [{letter}{nr + 1}]")
                    return

        # Rule 2: Uncover hidden neighbors when all mines
        # around a revealed clue have already been flagged.
        for row in range(board.getRows()):
            for col in range(board.getCols()):
                if board.getCellState(row, col) != 2:
                    continue

                hidden = []
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
                            hidden.append((nr, nc))
                        elif state in flagged_states:
                            flagged_count += 1

                clue = board.numBombNeighbors(row, col)

                if hidden and flagged_count == clue:
                    for nr, nc in hidden:
                        board.setState(nr, nc, False)
                        letter = chr(ord("A") + nc)
                        print(f"AI uncovered cell [{letter}{nr + 1}]")
                    return

        # Rule 3: Apply the additional 1-2-1 deduction.
        deduction = find_121_pattern(board)

        if deduction is not None:
            mines, safe_cells = deduction

            for row, col in mines:
                board.setState(row, col, True)
                letter = chr(ord("A") + col)
                print(f"AI flagged cell [{letter}{row + 1}]")

            for row, col in safe_cells:
                board.setState(row, col, False)
                letter = chr(ord("A") + col)
                print(f"AI uncovered cell [{letter}{row + 1}]")

            return

        # No deduction applies: make a random legal move.
        possible_cells = [
            (row, col)
            for row in range(board.getRows())
            for col in range(board.getCols())
            if board.getCellState(row, col) in hidden_states
        ]

        if possible_cells:
            row, col = random.choice(possible_cells)
            board.setState(row, col, False)
            letter = chr(ord("A") + col)
            print(f"AI uncovered cell [{letter}{row + 1}]")