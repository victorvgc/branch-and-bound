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
    constraint = []

    if '<=' in str_constraint:
        str_constraint = str_constraint.replace('<=,', '')
        # puts the constraint into an array
        str_split = str_constraint.split(',')
        constraint = [float(i) for i in str_split]

    if '>=' in str_constraint:
        str_constraint = str_constraint.replace('>=,', '')
        # puts the constraint into an array
        str_split = str_constraint.split(',')
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
            next_empty_row[i] = constraint[i]  # add the constraint into the next empty row
            i += 1

        next_empty_row[-1] = constraint[-1]
        next_empty_row[var + var_offset] = 1

    return tableau


def insert_obj_fun(tableau, str_obj_fun) -> np.array:
    """Insert the objective function into the tableau"""
    if can_insert_obj_fun(tableau):
        obj_fun = str_obj_fun.split(',')
        obj_fun = [float(i) for i in obj_fun]
        row_len = len(tableau[:, 0])

        last_empty_row = tableau[row_len - 1, :]

        i = 0
        while i < len(obj_fun) - 1:
            last_empty_row[i] = obj_fun[i] * -1  # add the objective function into the last empty row
            i += 1

        last_empty_row[-2] = 1  # put Z into the tableau
        last_empty_row[-1] = obj_fun[-1]

    return tableau


def next_round_r(tableau) -> bool:
    """Checks if pivots are required"""
    m = min(tableau[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


def next_round(tableau) -> bool:
    """Checks if pivots are required, therefore another iteration"""
    lr = len(tableau[:, 0])
    m = min(tableau[lr - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


def find_lowest_into_obj_fun(tableau):
    """Finds the column with the lowest value between variables of the objective function"""
    lr = len(tableau[:, 0])
    m = min(tableau[lr - 1, :-1])
    if m <= 0:
        n = np.where(tableau[lr - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


def find_lowest_element_into_constraints(tableau):
    """Finds the row of the lowest value between the constraints limits"""
    lc = len(tableau[0, :])
    m = min(tableau[:-1, lc - 1])
    if m <= 0:
        n = np.where(tableau[:-1, lc - 1] == m)[0][0]
    else:
        n = None
    return n


def loc_pivot_row(tableau):
    """Finds the pivot column and row. Used for pivoting the row"""
    total = []
    r = find_lowest_element_into_constraints(tableau)
    row = tableau[r, :-1]
    m = min(row)
    c = np.where(row == m)[0][0]
    col = tableau[:-1, c]
    for i, b in zip(col, tableau[:-1, -1]):
        if i != 0 and i ** 2 > 0 and b / i > 0:
            total.append(b / i)
        else:
            total.append(10000)
    index = total.index(min(total))
    return [index, c]


def loc_pivot_col(tableau):
    """Finds the pivot column and row. Used for pivoting the column"""
    if next_round(tableau):
        total = []
        n = find_lowest_into_obj_fun(tableau)
        for i, b in zip(tableau[:-1, n], tableau[:-1, -1]):
            if i != 0 and b / i > 0 and i ** 2 > 0:
                total.append(b / i)
            else:
                total.append(10000)
        index = total.index(min(total))
        return [index, n]


def pivot(row, col, tableau):
    """Pivot around the value into row and column assigned"""
    lr = len(tableau[:, 0])
    lc = len(tableau[0, :])
    t = np.zeros((lr, lc))
    pr = tableau[row, :]
    if tableau[row, col] ** 2 > 0:
        e = 1 / tableau[row, col]
        r = pr * e
        for i in range(len(tableau[:, col])):
            k = tableau[i, :]
            c = tableau[i, col]
            if list(k) == list(pr):
                continue
            else:
                t[i, :] = list(k - r * c)
        t[row, :] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')
