import typing
import unittest
import numpy as np

from csp import CSP


class TestCSP(unittest.TestCase):
            
    def test_additional_1(self):
            # Test whit a grid that starts with 0

            horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
            groups = horizontal_groups 
            constraints = [(3, 1), (3, 1)]

            valid_grid = np.array([[0,1],
                                [1,0]])
            csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
            result = csp.start_search()

            solution_grid = np.array([[2,1],
                                    [1,2]])
            
            self.assertTrue(np.all(solution_grid == result))

    def test_additional_2(self):
            #test to recognize count constraint

            groups = [[(0,0),(0,1),(1,0), (1,1)]]
            constraints = [(4, 2)] 

            valid_grid = np.array([[1,1],
                                [1,0]])
            
            csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
            result = csp.start_search()

            self.assertIsNone(result)


    
    def test_additional_3(self):
            # Test with unequal group sizes, and different count constraint

            group_1 = [(0,0),(0,2),(1,1),(1,2)]
            group_2 = [(0,1),(0,2),(1,2),(2,0)]
            group_3 = [(1,0),(2,1),(2,2)]

            groups = [group_1, group_2, group_3]
            constraints = [(9, 2), (9, 2), (9, 2)]

            valid_grid = np.array([[2,3,1],
                                [0,2,0],
                                [3,0,0]])
            
            csp = CSP(valid_grid, numbers=set([1,2,3]), groups=groups, constraints=constraints)
            result = csp.start_search()

            solution_grid = np.array([[2,3,1],
                                    [1,2,1],
                                    [3,1,2]])
            
            self.assertTrue(np.all(solution_grid == result))

            