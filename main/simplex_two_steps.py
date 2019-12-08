import numpy as np

from main import matrix_helper, simplex


def maximize(tableau) -> np.array:
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    artificial_var_size = get_artificial_var_size(tableau)
    if artificial_var_size > 0:
        tableau_two_steps = matrix_helper.gen_matrix(var_size, const_var_size, artificial_var_size)

        # preenche as variaveis artificiais no tableau de duas fases
        insert_artificial_row(tableau, tableau_two_steps, artificial_var_size)
        insert_artificial_columns(tableau, tableau_two_steps)

        total_var_size = var_size + const_var_size

        # preenche as variaveis do problema original no tableau de duas fases
        tableau_two_steps[:-1, :total_var_size] = tableau[:, :-1]

        # preenche os valores das restricoes e objetivo no tableau de duas fases
        tableau_two_steps[:-1, -1] = tableau[:, -1]

        # resolve o primeiro passo
        result = simplex.maximize(tableau_two_steps, var_size, const_var_size)

        # resolve o segundo passo
        tableau_two_steps = remove_artificial_row(tableau_two_steps)
        tableau_two_steps = remove_artificial_columns(tableau_two_steps, artificial_var_size)

        return simplex.maximize(tableau_two_steps, var_size, const_var_size, result['pivot_vars'])

    else:
        return simplex.maximize(tableau)


def minimize(tableau):
    tableau = convert_to_min(tableau)
    val = maximize(tableau)
    val['result'] = val['result'] * -1
    return val


def convert_to_min(tableau):
    """Converte um tableau de minimização para um de maximzação"""
    tableau[-1, :-1] = [-1 * i for i in tableau[-1, :-1]]
    tableau[-1, -1] = -1 * tableau[-1, -1]
    return tableau


def get_artificial_var_size(tableau) -> int:
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    const_col = tableau[:-1, -1]

    const_var_rows = tableau[:-1, var_size:-1]

    artificial_var_num = 0

    for i in range(const_var_size):
        s = const_var_rows[i, i]
        if s < 0 and (0 <= const_col[i]) or s == 0:
            artificial_var_num += 1

    return artificial_var_num


def insert_artificial_row(tableau, artificial_tableau, artificial_var_size):
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    artificial_col_len = len(artificial_tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    const_col = tableau[:-1, -1]

    const_var_rows = tableau[:-1, var_size:-1]

    artificial_rows = np.zeros((const_var_size, artificial_col_len))

    for i in range(const_var_size):
        s = const_var_rows[i, i]
        total = sum(const_col[:])
        if (s < 0 and (0 <= total)) or s == 0:
            artificial_rows[i, :-artificial_var_size - 1] = tableau[i, :-1]
            artificial_rows[i, -1] = tableau[i, -1]

    artificial_row = np.zeros((1, artificial_col_len))
    for row in artificial_rows:
        artificial_row[0, :] += row[:]

    artificial_row[0, :] = [float(i) * -1 for i in artificial_row[0, :]]

    artificial_tableau[-1, :-1] = artificial_row[0, :-1]
    artificial_tableau[-1, -1] = artificial_row[0, -1]


def insert_artificial_columns(tableau, artificial_tableau):
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])

    var_size = col_len - row_len
    const_var_size = row_len - 1

    var_offset = var_size + const_var_size

    const_col = tableau[:-1, -1]

    const_var_rows = tableau[:-1, var_size:-1]

    for i in range(const_var_size):
        s = const_var_rows[i, i]
        total = sum(const_col[:])
        if (s < 0 and (0 <= total)) or s == 0:
            artificial_tableau[i, var_offset] = 1
            var_offset += 1


def remove_artificial_row(artificial_tableau):
    artificial_tableau = np.delete(artificial_tableau, -1, 0)

    return artificial_tableau


def remove_artificial_columns(artificial_tableau, artificial_var_size):
    for i in range(artificial_var_size):
        artificial_tableau = np.delete(artificial_tableau, -2, 1)

    return artificial_tableau
