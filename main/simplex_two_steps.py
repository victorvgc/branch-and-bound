import numpy as np

from main import matrix_helper, simplex


def maximize(tableau, var=0, s_var=0) -> np.array:
    """Maximiza o PL inserido utilizando duas fases, caso necessario"""
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    if var == 0:
        var = col_len - row_len

    if s_var == 0:
        s_var = row_len - 1

    # verifica se ha necessidade de duas fases
    artificial_var_size = get_artificial_var_size(tableau)
    if artificial_var_size > 0:

        tableau_two_steps = matrix_helper.gen_matrix(var, s_var, artificial_var_size)

        # preenche as variaveis artificiais no tableau de duas fases
        insert_artificial_row(tableau, tableau_two_steps, artificial_var_size)
        insert_artificial_columns(tableau, tableau_two_steps)

        total_var_size = var + s_var

        # preenche as variaveis do problema original no tableau de duas fases
        tableau_two_steps[:-1, :total_var_size] = tableau[:, :-1]

        # preenche os valores das restricoes e objetivo no tableau de duas fases
        tableau_two_steps[:-1, -1] = tableau[:, -1]

        # resolve o primeiro passo
        result = simplex.maximize(tableau_two_steps, var, s_var, is_two_steps=True)

        # resolve o segundo passo
        tableau_two_steps = remove_artificial_row(tableau_two_steps)
        tableau_two_steps = remove_artificial_columns(tableau_two_steps, artificial_var_size)

        return simplex.maximize(tableau_two_steps, var, s_var, result['pivot_vars'])

    else:
        # caso nao necessite de duas fases, utiliza o simplex comum
        return simplex.maximize(tableau, var, s_var)


def minimize(tableau, var=0, s_var=0):
    """Minimiza o PL inserido utilizando duas fases, caso necessario"""
    tableau = convert_to_min(tableau)
    val = maximize(tableau, var, s_var)
    val['result'] = val['result'] * -1
    return val


def convert_to_min(tableau):
    """Converte um tableau de minimização para um de maximzação"""
    tableau[-1, :-1] = [-1 * i for i in tableau[-1, :-1]]
    tableau[-1, -1] = -1 * tableau[-1, -1]
    return tableau


def get_artificial_var_size(tableau) -> int:
    """Retorna a quantidade de variaveis artificiais necessarias"""
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
    """Insere linha com a funcao artificial"""
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
    """Insere as colunas das variaveis artificiais"""
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
    """Remove a linha com a funcao artificial"""
    artificial_tableau = np.delete(artificial_tableau, -1, 0)

    return artificial_tableau


def remove_artificial_columns(artificial_tableau, artificial_var_size):
    """Remove as colunas com as variaveis artificiais"""
    for i in range(artificial_var_size):
        artificial_tableau = np.delete(artificial_tableau, -2, 1)

    return artificial_tableau
