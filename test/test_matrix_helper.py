import unittest

import numpy as np

from main import matrix_helper


class MatrixHelperTest(unittest.TestCase):

    def test_if_generated_matrix_has_enough_space_and_is_all_zeros(self):
        # arrange
        var_count = 2
        constraint_count = 4

        # act
        result = matrix_helper.gen_matrix(var_count, constraint_count)

        # assert
        expected = np.zeros(((constraint_count + 1), (var_count + constraint_count + 2)))

        self.assertEqual(expected.all(), result.all())

    def test_if_can_insert_constraint_returns_true_when_tableau_is_empty(self):
        # arrange
        var_count = 2
        constraint_count = 4
        tableau = np.zeros(((constraint_count + 1), (var_count + constraint_count + 2)))

        # act
        result = matrix_helper.can_insert_constraint(tableau)

        # assert
        self.assertTrue(result)

    def test_if_can_insert_constraint_returns_false_when_tableau_is_not_empty(self):
        # arrange
        tableau = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0]])  # last row is for obj fun

        # act
        result = matrix_helper.can_insert_constraint(tableau)

        # assert
        self.assertFalse(result)

    def test_if_can_insert_obj_fun_returns_false_when_tableau_is_not_empty(self):
        # arrange
        tableau = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])

        # act
        result = matrix_helper.can_insert_obj_fun(tableau)

        # assert
        self.assertFalse(result)

    def test_if_can_insert_obj_fun_returns_true_when_tableau_has_only_one_empty_row(self):
        # arrange
        tableau_true = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0]])
        tableau_false = np.array([[1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 0, 0]])

        # act
        result_must_be_true = matrix_helper.can_insert_obj_fun(tableau_true)
        result_must_be_false = matrix_helper.can_insert_obj_fun(tableau_false)

        # assert
        self.assertFalse(result_must_be_false)
        self.assertTrue(result_must_be_true)

    def test_convert_string_to_constraint_lower_or_equal(self):
        # arrange
        str_constraint = '1, 1, <=, 1'

        # act
        result = matrix_helper.convert_string_to_constraint(str_constraint)

        # assert
        expected = np.array([1, 1, 1])

        self.assertEqual(expected.all(), result.all())

    def test_convert_string_to_constraint_higher_or_equal(self):
        # arrange
        str_constraint = '1, 1, >=, 1'

        # act
        result = matrix_helper.convert_string_to_constraint(str_constraint)

        # assert
        expected = np.array([-1, -1, -1])

        self.assertEqual(expected.all(), result.all())

    def test_if_insert_constraint_inserts_new_constraint(self):
        # arrange
        var_count = 2
        constraint_count = 4
        tableau = np.zeros(((constraint_count + 1), (var_count + constraint_count + 2)))
        constraint = '1, 1, >=, 1'

        # act
        result = matrix_helper.insert_constraint(tableau, constraint)

        # assert
        expected = np.array(
            [[0, 1, 1, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

        self.assertEqual(expected.all(), result.all())


if __name__ == '__main__':
    unittest.main()
