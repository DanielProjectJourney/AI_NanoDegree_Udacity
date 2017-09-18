assignments = []

# Referencing from Udacity AIND Sudoku Tutorial
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal Units
diagonal_units = [[row + col for row,col in zip(rows, cols)], [row + col for row, col in zip(rows[::-1], cols)]]

unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        # unit_value_list gets value values correponding to all box of a unit
        unit_value_list = [values[box] for box in unit]
        # naked_twin_value_list: list of naked twin in a unit - considered chance for multiple naked twin scenario in a unit
        naked_twin_value_list = list(set([box_val for box_val in unit_value_list \
                                          if len(box_val) == 2 and \
                                          unit_value_list.count(box_val) == 2]))

        for naked_twin_value in naked_twin_value_list:
            for digit_replace in naked_twin_value:
                for idx, unit_box_val in enumerate(unit_value_list):
                    if unit_box_val != naked_twin_value and len(unit_box_val) > 1:
                        # update the value with after removing digit of naked twin
                        values[unit[idx]] = values[unit[idx]].replace(digit_replace, '')

    return values


# Referencing from Udacity AIND Sudoku Tutorial
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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

# Referencing from Udacity AIND Sudoku Tutorial
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print(values)

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# Referencing from Udacity AIND Sudoku Tutorial
def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
            # values[peer] = values[peer].replace(digit,'')
    return values

# Referencing from Udacity AIND Sudoku Tutorial
def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:

        # the number of boxes have determined value --- Before Implementing Constraint Strategy
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Constraint Propagation
        # 1. Eliminate Strategy
        values = eliminate(values)

        # 2. Only Choice Strategy
        values = only_choice(values)

        # 3. Naked Twins Strategy
        values = naked_twins(values)

        # the number of boxes have determined value --- After Implementing Constraint Strategy
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])



        # Stop Constraint Propagation, when no new values be added.
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier in reduce_puzzle
    if all(len(values[s]) == 1 for s in values):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in values if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku,s,value)
        #new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = search(grid_values(grid))
    return  values

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
