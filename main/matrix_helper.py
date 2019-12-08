import numpy as np


def gen_matrix(var_size, constraint_size, artificial_var_size=0) -> np.array:
    """Gera um tableau para o problema de otimização"""
    # initializes the matrix with zeros
    if artificial_var_size > 0:
        tableau = \
            np.zeros(((constraint_size + 2), (var_size + artificial_var_size + constraint_size + 1)))
    else:
        tableau = np.zeros(((constraint_size + 1), (var_size + constraint_size + 1)))

    return tableau


def can_insert_constraint(tableau) -> bool:
    """Retorna True se o tableau pode receber uma restrição"""
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
    """Retorna True se o tableau pode receber a função objetivo"""
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
    """Converte uma string num array de restrição"""
    constraint = []

    if '<=' in str_constraint:
        str_constraint = str_constraint.replace('<=', '1')
        # puts the constraint into an array
        str_split = str_constraint.split(',')
        constraint = [float(i) for i in str_split]

    if '>=' in str_constraint:
        str_constraint = str_constraint.replace('>=', '-1')
        # puts the constraint into an array
        str_split = str_constraint.split(',')
        constraint = [float(i) for i in str_split]  # multiplying by -1 to invert the symbol

    if '=' in str_constraint:
        str_constraint = str_constraint.replace('=', '0')
        # puts the constraint into an array
        str_split = str_constraint.split(',')
        constraint = [float(i) for i in str_split]  # multiplying by -1 to invert the symbol

    return np.array(constraint)


def insert_constraint(tableau, constraint) -> np.array:
    """Insere uma restrição no tableau"""
    if can_insert_constraint(tableau):
        constraint = convert_string_to_constraint(constraint)
        col_len = len(tableau[0, :])
        row_len = len(tableau[:, 0])

        var = col_len - row_len
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
        while i < len(constraint) - 2:
            next_empty_row[i] = constraint[i]  # add the constraint into the next empty row
            i += 1

        next_empty_row[-1] = constraint[-1]
        next_empty_row[var + var_offset] = constraint[var]

    return tableau


def insert_obj_fun(tableau, str_obj_fun) -> np.array:
    """Insere a função objetivo no tableau"""
    if can_insert_obj_fun(tableau):
        obj_fun = str_obj_fun.split(',')
        obj_fun = [float(i) for i in obj_fun]
        row_len = len(tableau[:, 0])

        last_empty_row = tableau[row_len - 1, :]

        i = 0
        while i < len(obj_fun) - 1:
            last_empty_row[i] = obj_fun[i] * -1  # add the objective function into the last empty row
            i += 1

        last_empty_row[-1] = obj_fun[-1]

    return tableau


def next_iteration(tableau) -> bool:
    """Retorna True se necessario mais uma iteracao"""
    min_col = min(tableau[-1, :-1])

    return min_col < 0


def get_pivot(tableau) -> [int, int]:
    """Retorna as coordenadas do pivot"""
    m = min(tableau[-1, :-1])

    col = 0
    row = 0
    lowest = [0, 0]
    for i in tableau[-1, :-1]:
        if i == m:
            p_r = pivot_r(tableau, col, lowest[1])

            if p_r[1] < lowest[1] or lowest[1] == 0:
                row = p_r[0]
                lowest[0] = col
                lowest[1] = p_r[1]

        col += 1

    return [row, lowest[0]]


def pivot_r(tableau, pivot_column, min_div=0) -> [int, float]:
    """Retorna a linha e a razao minima do possivel pivo"""
    pivot_column = tableau[:-1, pivot_column]
    const_column = tableau[:-1, -1]

    row = 0
    lowest_r = 0
    for const, p in zip(const_column, pivot_column):
        if p != 0 and (min_div > const / p > 0 or (min_div == 0 and const / p > 0)):
            min_div = const / p
            lowest_r = row

        row += 1

    return [lowest_r, min_div]


def pivot_around(tableau, p_row, p_column) -> int:
    """
    Pivoteia em volta do pivo dado
    :param tableau:
    :param p_row:
    :param p_column:
    :return: -1 se impossivel
    """
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])

    if p_row >= row_len or p_column >= col_len:
        print('Problema impossivel')
        return -1

    p = tableau[p_row, p_column]

    for k in range(col_len):
        if tableau[p_row, k] != 0 and p != 0:
            tableau[p_row, k] = tableau[p_row, k] / p

    pivot_row = [i for i in tableau[p_row, :]]

    current_row_index = 0
    for current_row in tableau[:, :]:
        if current_row_index != p_row:
            row_coef = current_row[p_column]
            for k in range(col_len):
                current_row[k] = current_row[k] - row_coef * pivot_row[k]

        current_row_index += 1

    return 0
