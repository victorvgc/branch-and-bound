from main import matrix_helper


def maximize(tableau, var=0, s_var=0, pivot_vars=[], is_two_steps=False):
    """Maximiza o PL inserido"""
    val = {}
    result = 0

    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    if var == 0:
        var = col_len - row_len

    if s_var == 0:
        s_var = row_len - 1

    len_r = len(tableau[0, :-1])

    if len(pivot_vars) == 0:
        pivot_vars = get_pivot_vars(s_var)

    all_vars = get_vars(var, len_r)

    # Pivoteia enquanto houver proxima iteracao
    while matrix_helper.next_iteration(tableau) and result == 0:
        p = matrix_helper.get_pivot(tableau, is_two_steps)
        pivot_vars[p[0]] = all_vars[p[1]]
        result = matrix_helper.pivot_around(tableau, p[0], p[1])

    # Caso o resultado seja impossivel, cancela o metodo e retorna um erro
    if result == -1:
        val['result'] = 'Impossivel resolver'
        return val

    # Preenche o vetor de resultado de xn
    x_row = 0
    res_var = {}
    for x in pivot_vars:
        if 'x' in x and float(x.replace('x', '')) <= var:
            res_var[x] = tableau[x_row, -1]
        x_row += 1

    if len(res_var) < var:
        for x in range(var):
            if 'x' + str(x + 1) not in res_var:
                res_var['x' + str(x + 1)] = 0

    val['res_var'] = res_var

    # Preenche com o resultado da funcao objetivo
    val['result'] = tableau[-1, -1]

    # Preenche com as variaveis que entraram na base. Utilizado no Simplex de duas fases
    val['pivot_vars'] = pivot_vars
    # val['matrix'] = tableau
    return val


def minimize(tableau, var, s_var, pivot_vars=[]):
    """Minimiza o PL inserido invertendo os sinais para transformar em um problema de maximização"""
    tableau = convert_to_min(tableau)
    val = maximize(tableau, var, s_var, pivot_vars)
    val['result'] = val['result'] * -1
    # val['matrix'] = tableau
    return val


def convert_to_min(tableau):
    """Converte um tableau de minimização para um de maximzação"""
    tableau[-1, :-1] = [-1 * i for i in tableau[-1, :-1]]
    tableau[-1, -1] = -1 * tableau[-1, -1]
    return tableau


def get_vars(var, s_var):
    """Retorna um vetor com o nome de todas as variaveis do PL"""
    s = []
    for i in range(var):
        s.append('x' + str(i + 1))

    for i in range(s_var - var):
        s.append('s' + str(i + 1))

    return s


def get_pivot_vars(var):
    """Retorna um vetor com o nome das variaveis que entraram na base"""
    s = []
    for i in range(var):
        s.append('s' + str(i + 1))

    return s
