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

        #self.values = [False] * (num_vars + 1)
        self.values = [bool(random.getrandbits(1)) for i in range(self.num_vars + 1)]

        self.parse_sudoku_contraints(cnf_filename)
        #print(self.constraint_list)

    def parse_sudoku_contraints(self, cnf_filename):
        cnf_file = open(cnf_filename, 'r')
        constraints = cnf_file.readlines()

        for i in range(1000):
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
                self.var_map[int_var] = oint_var
                constraint_element.append(int_var)

            self.constraint_list.append(constraint_element)

    def random_assignment(self):
        self.values = [bool(random.getrandbits(1)) for i in range(self.num_vars + 1)]

    def walksat(self):
        for i in range(self.iteration_limit):
            if self.is_valid():
                self.iterations = i
                return self.values

            if random.random() > self.threshold:
                var_index = random.randint(1,self.num_vars)
                self.values[var_index] = not self.values[var_index]
            else:
                flip_list = self.get_best_flips()
                to_flip = random.choice(flip_list)
                self.values[to_flip] = not self.values[to_flip]

            if i%100 == 0:
                print("At iteration " + str(i) + ", with " + \
                        str(self.get_assignment_val()) + \
                        " constraints fulfilled out of " + str(len(self.constraint_list)))
            #else:
                #print("Iteration " + str(i))
        self.iterations = self.iteration_limit
        return None

    # Returns a list of all top scoring variables to flip
    def get_best_flips(self):
        flip_vals = []
        best_flips = []

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
        return best_flips

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
