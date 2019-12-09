import numpy as np

from main import simplex_two_steps, matrix_helper


def maximize(tableau, original=[], last_var_used=' '):
    highest = -1000000000  # visto que int nao possui valor -infinito

    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    s_var_size = row_len - 1

    original = gen_original_matrix(tableau)

    result = simplex_two_steps.maximize(tableau, var_size, s_var_size)

    if isinstance(result['result'], float):
        res = result['result']

        if res.is_integer():
            if res > highest:
                highest = result['result']

        if last_var_used.isspace():
            last_var_used = get_var(result['res_var'])
        else:
            last_var_used = get_var(result['res_var'], last_var_used)

        num_last_var = int(last_var_used.replace('x', ''))

        var_value = result['res_var'][last_var_used]
        r_const = generate_new_greater_constraint(num_last_var, var_size, var_value)
        l_const = generate_new_lower_constraint(num_last_var, var_size, var_value)

        right = gen_bnb_matrix(original)
        left = gen_bnb_matrix(original)

        matrix_helper.insert_vector_constraint(right, r_const)
        matrix_helper.insert_vector_constraint(left, l_const)

        r_res = maximize(right, original, last_var_used)
        l_res = maximize(left, original, last_var_used)

        res = r_res['result']
        if isinstance(res, float) and res.is_integer():
            if res > highest:
                highest = result['result']

        res = l_res['result']
        if isinstance(res, float) and res.is_integer():
            if res > highest:
                highest = result['result']

        result['result'] = highest

    return result


def generate_new_greater_constraint(num_las_var, var_size, var_value):
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
    row_len = len(tableau[:, 0])
    col_len = len(tableau[0, :])
    var_size = col_len - row_len
    const_var_size = row_len - 1

    original = np.zeros((const_var_size + 1, var_size + const_var_size + 1))
    original[:, :] = tableau[:, :]
    return original


def get_var(result, last_var=' '):
    for v in result:
        if 'x' in v:
            if not last_var.isspace():
                if int(last_var.replace('x', '')) < int(v.replace('x', '')):
                    return v
            else:
                return v

    return get_var(result)
