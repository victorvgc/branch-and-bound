from main import matrix_helper, simplex

if __name__ == '__main__':
    tableau = matrix_helper.gen_matrix(2, 4)

    print(tableau)

    tableau = matrix_helper.insert_constraint(tableau, '6,4,<=,24')
    tableau = matrix_helper.insert_constraint(tableau, '1,2,<=,6')
    tableau = matrix_helper.insert_constraint(tableau, '-1,1,<=,1')
    tableau = matrix_helper.insert_constraint(tableau, '0,1,<=,2')
    tableau = matrix_helper.insert_obj_fun(tableau, '5,4,0')

    print(tableau)

    print(simplex.maximize(tableau))
