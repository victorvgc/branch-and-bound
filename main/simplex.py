import numpy as np

from main.matrix_helper import next_round_r, pivot, loc_pivot_row, next_round, loc_pivot_col


def maximize(tableau):
    """
    Maximizes the operational problem
    :param tableau
    :return: Dictionary with the variable values and the result
    """
    while next_round_r(tableau):
        tableau = pivot(loc_pivot_row(tableau)[0], loc_pivot_row(tableau)[1], tableau)
    while next_round(tableau):
        tableau = pivot(loc_pivot_col(tableau)[0], loc_pivot_col(tableau)[1], tableau)
    lc = len(tableau[0, :])
    lr = len(tableau[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = tableau[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(tableau)[i]] = tableau[loc, -1]
        else:
            val[gen_var(tableau)[i]] = 0
    val['result'] = tableau[-1, -1]
    return val


def minimize(tableau):
    """
    Minimizes the operational problem through inverting the tableau to a maximizing problem.
    :param tableau
    :return: Dictionary with the variable values and the result
    """
    tableau = convert_to_min(tableau)
    val = maximize(tableau)
    val['result'] = val['result'] * -1
    return val


def convert_to_min(tableau):
    """Converts a tableau from minimizing to maximizing problem"""
    tableau[-1, :-2] = [-1 * i for i in tableau[-1, :-2]]
    tableau[-1, -1] = -1 * tableau[-1, -1]
    return tableau


def gen_var(table):
    """Generates an array with the variable names"""
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x' + str(i + 1))
    return v
