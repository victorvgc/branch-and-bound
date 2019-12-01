import numpy as np

"""Matrix helper

This script helps manipulating optimization problems matrices 

This script requires that `numpy` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * gen_matrix - Generates a matrix for the Optimization Problem
    * can_insert_constraint - Returns True if the tableau has space for another constraint
"""


def gen_matrix(var_count, constraint_count) -> np.array:
    """Generates a matrix for the Optimization Problem"""
    # initializes the matrix with zeros
    tableau = np.zeros(((constraint_count + 1), (var_count + constraint_count + 2)))
    return tableau


def can_insert_constraint(tableau) -> bool:
    """Returns True if the tableau has space for another constraint"""
    empty = 0  # number of empty rows
    row_len = len(tableau[:, 0])

    for i in range(row_len):
        total = 0
        for j in tableau[i, :]:
            total += j ** 2  # just to make j positive and assert that it is not 0

        if total == 0:  # then the row is empty
            empty += 1

    if empty > 1:  # then we have space for adding another constraint
        return True
    else:
        return False


def can_insert_obj_fun(tableau) -> bool:
    """Returns True if the tableau has space and is missing the objective function"""
    empty = 0  # number of empty rows
    row_len = len(tableau[:, 0])

    for i in range(row_len):
        total = 0
        for j in tableau[i, :]:
            total += j ** 2

        if total == 0:  # then the row is empty
            empty += 1

    if empty == 1:  # then only the objective function is missing
        return True
    else:
        return False


def convert_string_to_constraint(str_constraint) -> np.array:
    """Converts the string to a constraint array"""
    str_split = str_constraint.split(',')
    constraint = []

    if '<=' in str_split:
        symbol_index = str_split.index('<=')
        del str_split[symbol_index]
        # puts the constraint into an array
        constraint = [float(i) for i in str_split]

    if '>=' in str_split:
        symbol_index = str_split.index('>=')
        del str_split[symbol_index]
        # puts the constraint into an array
        constraint = [float(i) * -1 for i in str_split]  # multiplying by -1 to invert the symbol

    return np.array(constraint)


def insert_constraint(tableau, constraint) -> np.array:
    """Insert a constraint into the tableau"""
    if can_insert_constraint(tableau):
        constraint = convert_string_to_constraint(constraint)
        col_len = len(tableau[0, :])
        row_len = len(tableau[:, 0])

        var = col_len - row_len - 1
        var_offset = 0
        next_empty_row = np.array([])

        while var_offset < row_len:  # find the next empty row to insert the constraint
            next_empty_row = tableau[var_offset, :]
            total = 0
            for i in next_empty_row:
                total = i ** 2

            if total == 0:
                break

            var_offset += 1  # counts the number of constraints already added

        i = 0
        while i < len(constraint) - 1:
            next_empty_row[i] = constraint[i]  #

        next_empty_row[-1] = constraint[-1]
        next_empty_row[var + var_offset] = 1
