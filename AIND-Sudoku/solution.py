assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """ Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # we iterate through all columns in the Sudoku.
    for column_unit in unitlist:
        column_dict = {}
        # we iterate through all boxes in each column.
        for box in column_unit:
            column_dict[box] = values[box]

        col_values = list(column_dict.values())
        # for each column we create a set consisting of all naked twins (two digit values that occur only twice along that particular column.) that occur in that column.
        naked__twins = set([values[box] for box in column_dict if col_values.count(values[box]) == 2 and len(values[box]) == 2])
        # we then eliminate all occurence of digits contained in the naked__twins (set) ensuring we don't create an empty box.
        for box in column_unit:
            if values[box] in naked__twins:
                pass
            else:
                box_values = values[box]
                for element in naked__twins:
                    for digit_ in element:
                        if (digit_ in box_values) and len(box_values) > 1:
                            box_values = box_values.replace(digit_, "")
                values = assign_value(values, box, box_values)
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    return values


def cross(a, b):
    """Cross product of elements in A and elements in B.
    """

    return [s+t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    boxes = cross(rows, cols)
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = cross(rows, cols)
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        return False

    unfilled_squares = [box for box in boxes if len(values[box]) > 1]

    if len(unfilled_squares) == 0:
        # The sudoku has been completely solved.
        return values
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        fewest_value = '123456789'
        for box in unfilled_squares:
            if len(values[box]) <= len(fewest_value):
                fewest_value = values[box]
                best_box = box

        sudoku_tree = []
        sudoku = values.copy()

        for value in fewest_value:
            sudoku[best_box] = value
            sudoku_tree.append(sudoku)
            sudoku = values.copy()

        # Now use recursion to solve each one of the resulting sudoku, and if one returns a value (not False), return that answer!
        for sudoku in sudoku_tree:
            # Test if it fails after a sanity check.
            outcome = search(sudoku)
            if not outcome:
                pass
            else:
                unfilled_squares = [box for box in outcome.keys() if len(outcome[box]) > 1]
                if len(unfilled_squares) == 0:
                    return outcome
                else:
                    pass
    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    return solution


boxes = cross(rows, cols)
right_diagonal_units = [rows[cols.find(c)] + c for c in cols]
reversed_cols = cols[::-1]
col_index = len(cols)-1
left_diagonal_units = [rows[col_index - cols.find(c)] + c for c in reversed_cols]
diagonal_units = [left_diagonal_units, right_diagonal_units]
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
