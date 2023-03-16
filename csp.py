##################################################################################
# It is not allowed to add imports here. Use these two packages and nothing else.
import numpy as np
import typing
##################################################################################


class CSP:
    def __init__(self, grid:np.ndarray, numbers: typing.Set[int], groups: typing.List[typing.List[typing.Tuple[int,int]]],
                 constraints: typing.List[typing.Tuple[int,int]]):
        
        """
        The CSP solver object, containing all information and functions required for the assignment. You do not need to change
        this function.

        :param grid: 2-d numpy array corresponding to the grid that we have to fill in. Empty squares are denoted with 0s.
        :param numbers: The set of numbers that we are allowed to use in order to fill the grid (can be any set of integers)
        :param groups: A list of cell groups (cell groups are lists of location tuples).
        :param constraints: The list of constraints for every group of cells. constraints[i] hold for groups[i]. Every
                            constraint is a tuple of the form (sum_of_elements, max_count_element) where sum_of_elements 
                            indicates what the sum must be of the elements of the given group, and max_count_element indicates
                            the maximum number of times that a number/element may occur in the given group
        """

        self.width = grid.shape[1]
        self.height = grid.shape[0]
        self.numbers = numbers
        self.groups = groups
        self.constraints = constraints

        self.grid = grid
        self.cell_to_groups = {(row_idx, col_idx): [] for row_idx in range(self.height) for col_idx in range(self.width)}


    def fill_cell_to_groups(self):
        """
        Function that fills in the self.cell_to_groups datastructure, which maps a cell location (row_idx, col_idx)
        to a list of groups of which it is a member. For example, suppose that cell (0,0) is member of groups 0, 1,
        and 2. Then, self.cell_to_groups[(0,0)] should be equal to [0,1,2]. This function should do this for every cell. 
        If a cell is not a member of any groups, self.cell_to_groups[cell] should be an empty list []. 
        The function does not return anything. 

        Before completing this function, make sure to read the assignment description and study the data structures created
        in the __init__ function above (self.groups and self.cell_to_groups).
        """
        # loop through groups and add to cell_to_groups
        for i in range(self.height):
            for j in range(self.width):
                for a in range(len(self.groups)):
                    if self.groups[a].__contains__((i,j)):
                        self.cell_to_groups[(i,j)].append(a)


    def satisfies_sum_constraint(self, group: typing.List[typing.Tuple[int,int]], sum_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given sum constraint (group smaller or equal 
        than sum). Returns True if the current group satisfies the constraint and False otherwise. 

        :param group: The list of locations [first_cell, second_cell, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param sum_constraint: The sum_of_elements constraint specifying that the numbers in the given group must
                               sum up to this number. This is None if there is no sum constraint for the given group. 
        """

        #variable to hold sum of group
        sum = 0

        #loop through group and add to sum
        for i in range(len(group)):
            sum += self.grid[group[i]]

        # return true if sum is less than or equal to sum_constraint, false if not
        if sum <= sum_constraint:
            return True
        else:
            return False
        
    
    def satisfies_count_constraint(self, group: typing.List[typing.Tuple[int,int]], count_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given count constraint.
        Returns True if the current group satisfies the constraint and False otherwise. 
        Recall that the value of 0 indicates an empty cell (0s should not count towards the count constraint).

        :param group: The list of locations [first_cell, second_cell, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param count_constraint: Integer specifying that a given number cannot occur more than this amount of times. 
                                 This is None if there is no count constraint for the given group. 
        """

        # list to hold distinct values in group
        distinct_values = []

        # loop through group and add distinct values to list
        for i in range(len(group)):
            if (self.grid[group[i]] not in distinct_values) :
                distinct_values.append(self.grid[group[i]])
        
        # remove 0 from distinct_values
        if 0 in distinct_values:
            distinct_values.remove(0)

        # loop through distinct_values and count how many times each value occurs in group
        for i in range(len(distinct_values)):
            count = 0
            for j in range(len(group)):
                if distinct_values[i] == self.grid[group[j]]:
                    count += 1
            if count > count_constraint:
                return False
        
        return True
       


    def satisfies_group_constraints(self, group_indices: typing.List[int]) -> bool:
        """
        Function that checks whether the constraints for the given group indices are satisfied.
        Returns True if all relevant constraints are satisfied, False otherwise. Make sure to use functions defined above. 

        :param group_indices: The indices of the groups for which we check all of the constraints 
        """

        # check if constraints are satisfied
        for i in range(len(group_indices)):
            if self.satisfies_sum_constraint(self.groups[group_indices[i]], self.constraints[group_indices[i]][0]) == False:
                return False
            if self.satisfies_count_constraint(self.groups[group_indices[i]], self.constraints[group_indices[i]][1]) == False:
                return False

        return True    
    
                


    def search(self, empty_locations: typing.List[typing.Tuple[int, int]]) -> np.ndarray:
        """
        Recursive exhaustive search function. It tries to fill in the empty_locations with permissible values
        in an attempt to find a valid solution that does not violate any of the constraints. Instead of checking all
        possible constraints after filling in a number, it checks only the relevant group constraints using the 
        self.cell_to_groups data structure. 

        Returns None if there is no solution. Returns the filled in solution (self.grid) otherwise if a solution is found.

        :param empty_locations: list of empty locations that still need a value from self.numbers 
        """

        # Stopping condition for recursion: if there are no more empty locations, return the grid
        if len(empty_locations) == 0:
                    return self.grid
        
        # variable to check if last cell is reached
        final_Cell = False

        #first_cell and second_cell are the first two cells in empty_locations
        first_cell = empty_locations[0]

        # if there is more than one empty location, set second_cell to the second empty location
        if len(empty_locations) > 1:
            second_cell = empty_locations[1]

        # if no more empty locations, set FinalCell to True
        else:
            final_Cell = True

                

        #loop to start filling in the empty locations
        while empty_locations != []:
            
            # +1 to the first empty location for every iteration
            self.grid[first_cell] += 1

            # max_number to not exceed the biggest of self.numbers
            max_number = max(self.numbers)

            # if maxnumber is reached, no solution is found, so return None
            if self.grid[empty_locations[0]] > max_number:
                return None

            # if the first empty location satisfies the group constraints, check the second empty location
            if self.satisfies_group_constraints(self.cell_to_groups[empty_locations[0]]) == True:

                # if FinalCell is True, no need to check the second empty location
                if final_Cell == True:
                    return self.search(empty_locations[1:])

                #try to fill in the next empty location
                for i in range(len(self.numbers)):
                    self.grid[second_cell] += 1
                    if self.satisfies_group_constraints(self.cell_to_groups[second_cell]) == True:
                        
                        # As we check location by location, make second_cell zero before the recursive call
                        self.grid[second_cell] = 0 
                        
                        # if the second empty location satisfies the group constraints, recursively call the function to check the next empty location
                        return self.search(empty_locations[1:])

                # if no number satisfies the constraints, second_cell is set to 0 and first_cell is incremented by 1
                self.grid[second_cell] = 0

            elif self.satisfies_group_constraints(self.cell_to_groups[empty_locations[0]]) == False:
                continue

        # if no number satisfies the constraints, return None
        return None
        
        
    

    def start_search(self):
        """
        Non-recursive function that starts the recursive search function above. It first fills the cell_to_group
        data structure and computes the empty locations. Then, it starts the recursive search procedure. 
        The result is None if there is no solution possible. Otherwise, it returns the grid that is a solution.

        You do not need to change this function.
        """

        self.fill_cell_to_groups()
        empty_locations = [(row_idx, col_idx) for row_idx in range(self.height) for col_idx in range(self.width) if self.grid[row_idx,col_idx]==0]
        return self.search(empty_locations)
    
