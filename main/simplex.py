from main import matrix_helper


def maximize(tableau, var, s_var, pivot_vars=[]):
    """
        Maximiza o tableau inserido
        :param tableau contendo o problema de otimização
        :param var
        :param s_var
        :param pivot_vars
        :return: Dictionary {result, x1, x2,..., xn}
        """
    val = {}
    result = 0

    s_var = len(tableau[0, :-1]) - var

    if len(pivot_vars) == 0:
        pivot_vars = get_pivot_vars(s_var)

    all_vars = get_vars(var, s_var)

    while matrix_helper.next_iteration(tableau) and result == 0:
        p = matrix_helper.get_pivot(tableau)
        pivot_vars[p[0]] = all_vars[p[1]]
        result = matrix_helper.pivot_around(tableau, p[0], p[1])

    if result == -1:
        val['result'] = 'Impossivel resolver'
        return val

    x_row = 0
    res_var = {}
    for x in pivot_vars:
        if x != 1:
            res_var[x] = tableau[x_row, -1]
        x_row += 1

    val['res_var'] = res_var

    # for i in range(var):
    #     col = tableau[:, i]
    #     s = sum(col)
    #     m = max(col)
    #     if float(s) == float(m):
    #         loc = np.where(col == m)[0][0]
    #         val[gen_var(tableau)[i]] = tableau[loc, -1]
    #     else:
    #         val[gen_var(tableau)[i]] = 0

    val['result'] = tableau[-1, -1]
    val['pivot_vars'] = pivot_vars
    # val['matrix'] = tableau
    return val


def minimize(tableau, var, s_var, pivot_vars=[]):
    """
    Minimiza o tableau inserido invertendo os sinais para transformar em um problema de maximização.
    :param tableau contendo o problema de otimização
    :param tableau contendo o problema de otimização
    :param var
    :param s_var
    :param pivot_vars
    :return: Dictionary {result, x1, x2,..., xn}
    """
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
    s = []
    for i in range(var):
        s.append('x' + str(i + 1))

    for i in range(s_var):
        s.append('s' + str(i + 1))

    return s


def get_pivot_vars(var):
    s = []
    for i in range(var):
        s.append('s' + str(i + 1))

    return s
