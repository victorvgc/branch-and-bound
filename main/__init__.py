from main import matrix_helper, simplex
from main.matrix_helper import insert_obj_fun, gen_matrix, insert_constraint

if __name__ == '__main__':
    tableau = gen_matrix(2, 4)

    print(tableau)

    tableau = insert_constraint(tableau, '6,4,<=,24')
    tableau = insert_constraint(tableau, '1,2,<=,6')
    tableau = insert_constraint(tableau, '-1,1,<=,1')
    tableau = insert_constraint(tableau, '0,1,<=,2')
    tableau = insert_obj_fun(tableau, '5,4,0')

    print(tableau)

    print(simplex.maximize(tableau))
