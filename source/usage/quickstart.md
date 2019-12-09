Como utilizar
============================================

## Simplex comum

### Maximizacao

    tableau = gen_matrix(2, 4)

    tableau = insert_constraint(tableau, '6,4,<=,24')
    tableau = insert_constraint(tableau, '1,2,<=,6')
    tableau = insert_constraint(tableau, '-1,1,<=,1')
    tableau = insert_constraint(tableau, '0,1,<=,2')
    tableau = insert_obj_fun(tableau, '5,4,0')

    result = simplex.maximize(tableau)

    print(result['res_var'])
    print(result['result'])

## Simplex de duas fases

### Maximizacao

    tableau = gen_matrix(3, 3)

    tableau = insert_constraint(tableau, '2,1,-1,<=,10')
    tableau = insert_constraint(tableau, '1,1,2,>=,20')
    tableau = insert_constraint(tableau, '2,1,3,=,60')
    tableau = insert_obj_fun(tableau, '1,1,1,0')

    result = simplex_two_steps.maximize(tableau)

    print(result['res_var'])
    print(result['result'])
    
### Minimizacao
    
    tableau = gen_matrix(2, 3)

    tableau = insert_constraint(tableau, '1,1,>=,2')
    tableau = insert_constraint(tableau, '-1,1,>=,1')
    tableau = insert_constraint(tableau, '0,1,<=,3')
    tableau = insert_obj_fun(tableau, '1,-2,0')

    result = simplex_two_steps.minimize(tableau)

    print(result['res_var'])
    print(result['result'])

## Branch and Bound

### Maximizacao

    tableau = gen_matrix(2, 2)

    tableau = insert_constraint(tableau, '1,1,<=,6')
    tableau = insert_constraint(tableau, '5,9,<=,45')
    tableau = insert_obj_fun(tableau, '5,8,0')

    result = branch_and_bound.maximize(tableau)

    print(result['res_var'])
    print(result['result'])
    
### Minimizacao

    tableau = gen_matrix(2, 2)

    tableau = insert_constraint(tableau, '6,7,>=,40')
    tableau = insert_constraint(tableau, '0,1,>=,2')
    tableau = insert_obj_fun(tableau, '6,8,0')

    result = branch_and_bound.minimize(tableau)
    print(result['res_var'])
    print(result['result'])