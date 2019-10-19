from Sudoku import Sudoku
import random
from heapq import heappush, heappop
class SAT:

    def __init__(self, cnf_filename, num_vars, var_start = 0, threshold = .7, iteration_lim = 100000):
        self.constraint_list = []
        self.iterations = 0
        self.iteration_limit = iteration_lim
        self.threshold = threshold
        self.num_vars = num_vars
        self.var_start = var_start
        self.var_map = {}
        self.const_vars = set()

        self.values = [bool(random.getrandbits(1)) for i in range(self.num_vars + 1)]

        self.parse_sudoku_contraints(cnf_filename)


    def parse_sudoku_contraints(self, cnf_filename):
        cnf_file = open(cnf_filename, 'r')
        constraints = cnf_file.readlines()

        for i in range(111, 1000):
            if i % 10 != 0 and (i//10)%10 != 0:
                int_var = i - 110
                int_var -= int_var//10 + 9*((int_var)//100)
                self.var_map[int_var] = i

        # Read constraints into set of sets of variables. Each set in
        # constraint_set represents one or statement of all included variables
        for constraint in constraints:
            constraint_element = []
            for var in constraint.split():
                oint_var = int(var)
                if oint_var < 0:
                    int_var = oint_var + self.var_start
                    int_var += (-int_var)//10 + 9*((-int_var)//100)
                else:
                    int_var = oint_var - self.var_start
                    int_var -= int_var//10 + 9*((int_var)//100)
                constraint_element.append(int_var)

            # LIMITS KNOWN VARS
            if len(constraint_element) == 1:
                var = constraint_element[0]
                if var > 0:
                    self.values[var] = True
                    self.const_vars.add(var)
                else:
                    self.values[-var] = False
                    self.const_vars.add(-var)

            self.constraint_list.append(constraint_element)
        cnf_file.close()


    def walksat(self):
        hits  = 0
        for i in range(self.iteration_limit):
            clause = self.get_invalid_clause()

            # Avoids having to check validity and get invalid clause separately
            if clause is None:
                self.iterations = i
                return self.values

            if random.random() > self.threshold:
                var_index = random.choice(clause)
                if var_index < 0:
                    var_index = -var_index
                if var_index not in self.const_vars:
                    self.values[var_index] = not self.values[var_index]
                else: #Debugging
                    hits += 1
            else:
                to_flip = self.get_clause_flip(clause)
                if to_flip < 0:
                    to_flip = -to_flip

                if to_flip not in self.const_vars:
                    self.values[to_flip] = not self.values[to_flip]
                else: #Debugging
                    hits += 1

            if i%100 == 0:
                print("At iteration " + str(i) + ", with " + \
                        str(self.get_assignment_val()) + \
                        " constraints fulfilled out of " + str(len(
                        self.constraint_list)) + " and " + str(hits) + " hits.")

    # Gets a random invalid clause from the list of constraints
    def get_invalid_clause(self):
        invalid = []
        for constraint in self.constraint_list:
            valid = False
            for var in constraint:
                if var > 0 and self.values[var]:
                    valid = True
                    break
                if var < 0 and not self.values[-var]:
                    valid = True
                    break

            if not valid:
                invalid.append(constraint)
        if len(invalid) == 0:
            return None
        else:
            return random.choice(invalid)

    # Returns a list of all top scoring variables to flip
    def get_best_flip(self):
        flip_vals = []
        best_flips = []

        # Flip all vars, scoring the assignment with the var flipped
        for i in range(1, self.num_vars + 1):
            self.values[i] = not self.values[i]
            flip_val = -1 * self.get_assignment_val()
            self.values[i] = not self.values[i]

            heappush(flip_vals, (flip_val, i))

        curr_var = heappop(flip_vals)
        best_flips.append(curr_var[1])
        last_val = curr_var[0]

        while len(flip_vals) > 0:
            curr_var = heappop(flip_vals)
            if curr_var[0] == last_val:
                best_flips.append(curr_var[1])
                last_val = curr_var[0]
            else:
                break
        return random.choice(best_flips)

    # Get best flip within a clause
    def get_clause_flip(self, clause):
        flip_vals = []
        best_flips = []
        for var in clause:
            self.values[var] = not self.values[var]
            flip_val = -1 * self.get_assignment_val()
            self.values[var] = not self.values[var]

            heappush(flip_vals, (flip_val, var))

        curr_var = heappop(flip_vals)
        best_flips.append(curr_var[1])
        last_val = curr_var[0]

        while len(flip_vals) > 0:
            curr_var = heappop(flip_vals)
            if curr_var[0] == last_val:
                best_flips.append(curr_var[1])
                last_val = curr_var[0]
            else:
                break
        return random.choice(best_flips)

    # Returns the number of constraints fulfilled by an assignment
    def get_assignment_val(self):
        assignment_val = 0
        valid = False

        for constraint in self.constraint_list:
            valid = False
            #print(str(constraint))
            for var in constraint:
                if var > 0 and self.values[var]:
                    valid = True
                    break
                if var < 0 and not self.values[-var]:
                    valid = True
                    break
            if valid:
                assignment_val += 1
        return assignment_val

    # Checks if an assignment fulfils all constraints
    def is_valid(self):
        for constraint in self.constraint_list:
            valid = False
            for var in constraint:
                if var > 0 and self.values[var]:
                    valid = True
                    break
                if var < 0 and not self.values[-var]:
                    valid = True
                    break
            if not valid:
                #print("Constraint " + str(constraint) + " violated.")
                return False
        return True

    def write_solution(self, sol_filename):
        sol_file = open(sol_filename, 'w')
        for i in range(1, len(self.values)):
            if self.values[i]:
                #print("writing " + str(i + self.var_start))
                sol_file.write(str(self.var_map[i]))
                sol_file.write("\n")
            else:
                #print("writing " + str(-i - self.var_start))
                sol_file.write(str(-self.var_map[i]))
                sol_file.write("\n")
        #print(str(self.values))



#
