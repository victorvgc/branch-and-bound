import numpy as np

from main import simplex_two_steps, matrix_helper


def maximize(tableau, original=[], last_var_used=' ', best_solution=-1000000000, has_constraints_on=[], var_size=0):
    """Maximiza o PL com x1, x2, ..., xn inteiros"""
    highest = -1000000000  # visto que int nao possui valor -infinito

    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    if var_size == 0:
        var_size = col_len - row_len

    s_var_size = row_len - 1

    original = gen_original_matrix(tableau)

    result = simplex_two_steps.maximize(tableau, var_size, s_var_size)

    if isinstance(result['result'], float):
        if best_solution == -1000000000:
            best_solution = result['result']

        if is_a_viable_solution(result):
            return result

        # pega a proxima variavel a ser limitada
        if last_var_used.isspace():
            last_var_used = get_var(result['res_var'])
        else:
            last_var_used = get_var(result['res_var'], last_var_used)

        num_last_var = int(last_var_used.replace('x', ''))

        add_constrained_var(has_constraints_on, last_var_used)

        # gera novas restricoes
        var_value = result['res_var'][last_var_used]
        r_const = generate_new_greater_constraint(num_last_var, var_size, var_value)
        l_const = generate_new_lower_constraint(num_last_var, var_size, var_value)

        original = evaluate_add_new_constraint(original, num_last_var)

        # gera as novas tableaux
        right = gen_bnb_matrix(original)
        left = gen_bnb_matrix(original)

        matrix_helper.insert_vector_constraint(right, r_const)
        matrix_helper.insert_vector_constraint(left, l_const)

        # gera dois novos galhos
        if is_possible_right(result, best_solution):  # avalia se e possivel continuar para a direita
            r_res = maximize(right, original, last_var_used, best_solution, var_size=var_size)

            if isinstance(r_res['result'], float) and r_res['result'] > highest:
                result = r_res
                highest = r_res['result']

        l_res = maximize(left, original, last_var_used, best_solution, var_size=var_size)

        if isinstance(l_res['result'], float) and l_res['result'] > highest:
            result = l_res

    return result


def minimize(tableau, original=[], last_var_used=' ', best_solution=1000000000, has_constraints_on=[], var_size=0):
    """Minimiza o PL com x1, x2, ..., xn inteiros"""
    lowest = 1000000000  # visto que int nao possui valor infinito

    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    if var_size == 0:
        var_size = col_len - row_len

    s_var_size = row_len - 1

    original = gen_original_matrix(tableau)

    result = simplex_two_steps.minimize(tableau, var_size, s_var_size)

    if isinstance(result['result'], float):
        if best_solution == 1000000000:
            best_solution = result['result']

        if is_a_viable_solution(result):
            return result

        if not has_solution(result):
            result['result'] = 'Solucao inviavel'
            return result

        # pega a proxima variavel a ser limitada
        if last_var_used.isspace():
            last_var_used = get_var(result['res_var'])
        else:
            last_var_used = get_var(result['res_var'], last_var_used)

        num_last_var = int(last_var_used.replace('x', ''))

        add_constrained_var(has_constraints_on, last_var_used)

        # gera novas restricoes
        var_value = result['res_var'][last_var_used]
        r_const = generate_new_greater_constraint(num_last_var, var_size, var_value)
        l_const = generate_new_lower_constraint(num_last_var, var_size, var_value)

        original = evaluate_add_new_constraint(original, num_last_var)

        # gera as novas tableaux
        right = gen_bnb_matrix(original)
        left = gen_bnb_matrix(original)

        matrix_helper.insert_vector_constraint(right, r_const)
        matrix_helper.insert_vector_constraint(left, l_const)

        # gera dois novos galhos
        r_res = minimize(right, original, last_var_used, best_solution, var_size=var_size)

        if isinstance(r_res['result'], float) and r_res['result'] < lowest:
            result = r_res
            lowest = r_res['result']

        if is_possible_left(result, best_solution):  # avalia se e possivel continuar para a esquerda
            l_res = minimize(left, original, last_var_used, best_solution, var_size=var_size)

            if isinstance(l_res['result'], float) and l_res['result'] < lowest:
                result = l_res

    return result


def generate_new_greater_constraint(num_las_var, var_size, var_value):
    """Gera uma nova restricao de >= para o PL"""
    constraint = []
    for i in range(var_size):
        if i != num_las_var - 1:
            constraint.append(0)
        else:
            constraint.append(1)

    constraint.append(-1)
    v = round(var_value)

    if v > var_value:
        constraint.append(v)
    else:
        constraint.append(v + 1)

    return constraint


def generate_new_lower_constraint(num_las_var, var_size, var_value):
    """Gera uma nova restricao de <= para  PL"""
    constraint = []
    for i in range(var_size):
        if i != num_las_var - 1:
            constraint.append(0)
        else:
            constraint.append(1)

    constraint.append(1)

    v = round(var_value)

    if v > var_value:
        constraint.append(v - 1)
    else:
        constraint.append(v)

    return constraint


def gen_bnb_matrix(tableau):
    """Gera um novo tableau para comportar a nova restricao"""
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    bnb_tableau = np.zeros((const_var_size + 2, var_size + const_var_size + 2))
    bnb_tableau[:-2, :-2] = tableau[:-1, :-1]
    bnb_tableau[-1, :-2] = tableau[-1, :-1]
    bnb_tableau[:-2, -1] = tableau[:-1, -1]
    bnb_tableau[-1, - 1] = tableau[-1, -1]

    return bnb_tableau


def gen_original_matrix(tableau):
    """Copia tableau passado"""
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    original = np.zeros((const_var_size + 1, var_size + const_var_size + 1))
    original[:, :] = tableau[:, :]
    return original


def get_var(result, last_var=' '):
    """Retorna a proxima variavel a ser restringida"""
    for v in result:
        if 'x' in v:
            if not last_var.isspace():
                if int(last_var.replace('x', '')) < int(v.replace('x', '')):
                    return v
            else:
                return v

    return get_var(result)


def is_a_viable_solution(result):
    """Verifica se a solucao e viavel"""
    res = result['result']
    res_var = result['res_var']

    if isinstance(res, float) and res.is_integer():
        for x in result['res_var']:
            if 'x' in x:
                if isinstance(res_var[x], float) and res_var[x].is_integer():
                    continue
                else:
                    return False

        return True
    else:
        return False


def is_possible_right(result, best):
    """Verifica se a solucao mais a direira e possivel"""
    res = result['result']

    if isinstance(res, float):
        if res != best:
            if res.is_integer():
                if res + 1 > best:
                    return False
                else:
                    return True

        return True

    return False


def is_possible_left(result, best):
    """Verifica se a solucao mais a esquerda e possivel"""
    res = result['result']

    if isinstance(res, float):
        if res != best:
            if res.is_integer():
                if res - 1 < best:
                    return False
                else:
                    return True

        return True

    return False


def add_constrained_var(has_const_on, x):
    """Adiciona xn ao vetor de controle de variaveis ja rstringidas"""
    for cx in has_const_on:
        if cx == x:
            return

    has_const_on.append(x)


def find_constraint_row(tableau, x):
    """Retorna a linha de restricao de x"""
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len

    row_index = 0
    for row in tableau[:-1, :-1]:
        v = 0
        for k in range(var_size):
            v += row[k] ** 2

        if v == 1:
            v_index = 0
            for r in row:
                if r == 1:
                    break
                v_index += 1

            if x - 1 == v_index:
                return {'t': tableau[row_index, :], 'r': row_index}

        row_index += 1

    return {'t': tableau[row_index, :], 'r': -1}


def find_constraint_col(row):
    """Retorna a coluna de restricao da linha"""
    col_index = 0

    v = 0
    for r in row:
        v += r ** 2
        if v == 2:
            return col_index

        col_index += 1


def evaluate_add_new_constraint(tableau, last_var):
    """Avalia e remove restricoes desnecessarias"""
    row_to_delete = find_constraint_row(tableau, last_var)
    if row_to_delete['r'] != -1:
        col_to_delete = find_constraint_col(row_to_delete['t'])
        tableau = np.delete(tableau, row_to_delete['r'], 0)
        tableau = np.delete(tableau, col_to_delete, 1)

    return tableau


def has_solution(result):
    """Avalia se o resultado atual e uma solucao"""
    pivot_vars = result['pivot_vars']

    for v in pivot_vars:
        if 'x' in v:
            return True

    return False
