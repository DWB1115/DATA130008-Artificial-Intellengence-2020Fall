import copy
from csp import CSP


def create_n_queens_csp(n=8):
    """Create an N-Queen problem on the board of size n * n.

    You should call csp.add_variable() and csp.add_binary_factor().

    Args:
        n: int, number of queens, or the size of one dimension of the board.

    Returns
        csp: A CSP problem with correctly configured factor tables
        such that it can be solved by a weighted CSP solver
    """
    csp = CSP()
    # TODO: Problem b
    # TODO: BEGIN_YOUR_CODE
    # Queens is a list of variables, which denote the position of the queen in each row
    # Queens is defined as 'Qi', where i is the row of a queen
    Queens = ['Q' + str(i+1) for i in range(n)]
    value_list = [i+1 for i in range(n)]
    for queen in Queens:
        csp.add_variable(queen, value_list)
    # binary_factor: two queens can't in the same column, and duijiaoxian
    for queen1 in Queens:
        for queen2 in Queens:
            if queen1 != queen2:
                # Using the define 'Qi', to get i
                row1 = int(queen1.split('Q')[1])
                row2 = int(queen2.split('Q')[1])
                delta = abs(row1 - row2)
                csp.add_binary_factor(queen1, queen2, lambda x, y: x != y and abs(x-y) != delta)
    # TODO: END_YOUR_CODE
    return csp


class BacktrackingSearch:
    """A backtracking algorithm that solves CSP.

    Attributes:
        num_assignments: keep track of the number of assignments
            (identical when the CSP is unweighted)
        num_operations: keep track of number of times backtrack() gets called
        first_assignment_num_operations: keep track of number of operations to
            get to the very first successful assignment (maybe not optimal)
        all_assignments: list of all solutions found

        csp: a weighted CSP to be solved
        mcv: bool, if True, use Most Constrained Variable heuristics
        ac3: bool, if True, AC-3 will be used after each variable is made
        domains: dictionary of domains of every variable in the CSP

    Usage:
        search = BacktrackingSearch()
        search.solve(csp)
    """

    def __init__(self):
        self.num_assignments = 0
        self.num_operations = 0
        self.first_assignment_num_operations = 0
        self.all_assignments = []

        self.csp = None
        self.mcv = False
        self.ac3 = False
        self.domains = {}

    def reset_results(self):
        """Resets the statistics of the different aspects of the CSP solver."""
        self.num_assignments = 0
        self.num_operations = 0
        self.first_assignment_num_operations = 0
        self.all_assignments = []

    def check_factors(self, assignment, var, val):
        """Check consistency between current assignment and a new variable.

        Given a CSP, a partial assignment, and a proposed new value for a
        variable, return the change of weights after assigning the variable
        with the proposed value.

        Args:
            assignment: A dictionary of current assignment.
                Unassigned variables do not have entries, while an assigned
                variable has the assigned value as value in dictionary.
                e.g. if the domain of the variable A is [5,6],
                and 6 was assigned to it, then assignment[A] == 6.
            var: name of an unassigned variable.
            val: the proposed value.

        Returns:
            bool
                True if the new variable with value can satisfy constraint,
                otherwise, False
        """
        assert var not in assignment
        if self.csp.unary_factors[var]:
            if self.csp.unary_factors[var][val] == 0:
                return False
        for var2, factor in self.csp.binary_factors[var].items():
            if var2 not in assignment:
                continue
            if factor[val][assignment[var2]] == 0:
                return False
        return True

    def solve(self, csp, mcv=False, ac3=False):
        """Solves the given unweighted CSP using heuristics.

        Note that we want this function to find all possible assignments.
        The results are stored in the variables described in
            reset_result().

        Args:
            csp: A unweighted CSP.
            mcv: bool, if True, Most Constrained Variable heuristics is used.
            ac3: bool, if True, AC-3 will be used after each assignment of an
            variable is made.
        """
        self.csp = csp
        self.mcv = mcv
        self.ac3 = ac3
        self.reset_results()
        self.domains = {var: list(self.csp.values[var])
                        for var in self.csp.variables}
        self.backtrack({})

    def backtrack(self, assignment):
        """Back-tracking algorithms to find all possible solutions to the CSP.

        Args:
            assignment: a dictionary of current assignment.
                Unassigned variables do not have entries, while an assigned
                variable has the assigned value as value in dictionary.
                    e.g. if the domain of the variable A is [5, 6],
                    and 6 was assigned to it, then assignment[A] == 6.
        """
        self.num_operations += 1

        num_assigned = len(assignment.keys())
        if num_assigned == self.csp.vars_num:
            self.num_assignments += 1
            new_assignment = {}
            for var in self.csp.variables:
                new_assignment[var] = assignment[var]
            self.all_assignments.append(new_assignment)
            if self.first_assignment_num_operations == 0:
                self.first_assignment_num_operations = self.num_operations
            return

        var = self.get_unassigned_variable(assignment)
        ordered_values = self.domains[var]

        if not self.ac3:
            # TODO: Problem a
            # TODO: BEGIN_YOUR_CODE
            for value in ordered_values:
                if self.check_factors(assignment, var, value):
                    assignment[var] = value
                    self.backtrack(assignment)
                    del assignment[var]
            # TODO: END_YOUR_CODE

        else:
            # TODO: Problem d
            # TODO: BEGIN_YOUR_CODE
            for value in ordered_values:
                if self.check_factors(assignment, var, value):
                    assignment[var] = value
                    domin_copy = copy.deepcopy(self.domains)
                    self.domains[var] = [value]
                    succeed = self.arc_consistency_check(var)
                    if succeed:
                        self.backtrack(assignment)
                    self.domains = domin_copy
                    del assignment[var]
            # TODO: END_YOUR_CODE

    def get_unassigned_variable(self, assignment):
        """Get a currently unassigned variable for a partial assignment.

        If mcv is True, Use heuristic: most constrained variable (MCV)
        Otherwise, select a variable without any heuristics.

        Most Constrained Variable (MCV):
            Select a variable with the least number of remaining domain values.
            Hint: self.domains[var] gives you all the possible values
            Hint: choose the variable with lowest index in self.csp.variables
                for ties
        Args:
            assignment: a dictionary of current assignment.

        Returns
            var: a currently unassigned variable.
        """
        if not self.mcv:
            for var in self.csp.variables:
                if var not in assignment:
                    return var
        else:
            # TODO: Problem c
            # TODO: BEGIN_YOUR_CODE
            # sort the number of leaving values for each variable
            var_dict = dict()    # key:a variable, value:number of leaving values for it
            for var in self.csp.variables:
                if var not in assignment:
                    count = 0
                    for value in self.domains[var]:
                        if self.check_factors(assignment, var, value):
                            count += 1
                    var_dict[var] = count
            count_list = list(var_dict.items())
            count_list.sort(key = lambda x: x[1])
            return count_list[0][0]
        """
        I don't know why the code below can't get grade
            #var_left = list(set(self.csp.variables) - set(assignment))
            # for var in var_left:
            #     count = 0
            #     for value in self.domains[var]:
            #         if self.check_factors(assignment, var, value):
            #             count += 1
            #     var_dict[var] = count
            # count_list = list(var_dict.items())
            # count_list.sort(key = lambda x: x[1])
            # return count_list[0][0]
        """
            # TODO: END_YOUR_CODE

    def arc_consistency_check(self, var):
        """AC-3 algorithm.

        The goal is to reduce the size of the domain values for the unassigned
        variables based on arc consistency.

        Hint: get variables neighboring variable var:
            self.csp.get_neighbor_vars(var)

        Hint: check if a value or two values are inconsistent:
            For unary factors
                self.csp.unaryFactors[var1][val1] == 0
            For binary factors
                self.csp.binaryFactors[var1][var2][val1][val2] == 0

        Args:
            var: the variable whose value has just been set

        Returns
            boolean: succeed or not
        """
        # TODO: Problem d
        # TODO: BEGIN_YOUR_CODE
        # initialize the queue
        neighbors = list(self.csp.get_neighbor_vars(var))
        queue = [(neighbor, var) for neighbor in neighbors]
        for var1 in self.csp.variables:
            for var2 in self.csp.variables:
                if var1 != var2:
                    queue.append((var1,var2))
        # begin arc-consistant-test
        while len(queue):
            var1, var2 = queue.pop(0)
            for val1 in self.domains[var1]:
                sign = 0
                for val2 in self.domains[var2]:    
                    if self.csp.binary_factors[var1][var2][val1][val2]:
                        sign = 1
                if sign == 0:
                    self.domains[var1].remove(val1)
                    if len(self.domains[var1]) == 0:
                        return False
                    new_nei = list(self.csp.get_neighbor_vars(var1))
                    new_add = [(neighbor, var1) for neighbor in new_nei]
                    queue += new_add
        return True
        
        # TODO: END_YOUR_CODE
