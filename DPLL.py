from Sudoku import Sudoku
import random
from heapq import heappush, heappop

class DPLL:

    def __init__(self, cnf_filename, num_vars, var_start = 0, depth_lim=1000):
        self.constraint_list = []
        self.iterations = 0
        self.num_vars = num_vars
        self.var_start = var_start
        self.var_map = {}
        self.depth_lim = depth_lim
        self.model = None
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

            self.constraint_list.append(constraint_element)
        cnf_file.close()

    # Sets initial purity dictionary
    def parse_purities(self, purity_dict, model):
        vars = range(1, self.num_vars + 1)

        # Initialize purity dictionary
        for var in vars:
            purity_dict[var] = 0
            purity_dict[-var] = 0

        # Update purity dictionary with clauses
        for var in range(1, self.num_vars + 1):
            for clause in self.constraint_list:
                if var in clause:
                    purity_dict[var] += 1
                if -var in clause:
                    purity_dict[-var] += 1

            # Pure variables
            if purity_dict[var] == 0:
                if var not in model:
                    model.add(-var)
            elif purity_dict[-var] == 0:
                if -var not in model:
                    model.add(var)
        #print("Purity dict: " + str(purity_dict))


    def init_dpll(self):
        model = set()
        purity_dict = {}
        pure_list = []
        self.parse_purities(purity_dict, model)
        self.model = self.run_dpll(model, purity_dict, 0)
        return self.model


    # Recursive element
    def run_dpll(self, model, purity_dict, depth):
        #print("================")
        #print("Model is: ")
        #print(model)
        #print("At depth " + str(depth))
        #print("================")
        validity = self.is_valid(model)
        if validity == 1:
            return model
        elif depth > self.depth_lim:
            print('Depth limit exceeded')
            return False
        elif validity == 0:
            #print("Failed at depth " + str(depth))
            return False

        # Unit Clause Check
        (vals, clauses) = self.get_unit_clauses(model)

        if vals is not None:
            next_model = model.copy()
            next_purity = purity_dict.copy()
            for clause in clauses:
                for var in clause:
                    next_purity[var] -= 1 # These clauses are fulfilled now
                    if next_purity[var] == 0: # Variable is now pure
                        if var not in next_model:
                            next_model.add(-var)
            for val in vals:
                if -val not in next_model:
                    next_model.add(val)
                else: # Conflict!
                    return False

            return self.run_dpll(next_model, next_purity, depth + 1)

        # Random Assignment Step
        chosen_var = self.get_rand_unassigned(model)
        if chosen_var is None: # No unassigned vars - need to check validity
            validity = self.is_valid(model)
            if validity == 1:
                return values
            print("No unassigned variable found but model is not valid.")
            print("Model: ")
            print(model)
            return False

        next_model = model.copy()
        next_purity = purity_dict.copy()
        next_model.add(chosen_var)
        self.check_purities(next_model, next_purity, chosen_var)
        next_values = self.run_dpll(next_model, next_purity, depth + 1)
        if next_values:
            return next_values


        next_model = model.copy()
        next_purity = purity_dict.copy()
        next_model.add(-chosen_var)
        self.check_purities(next_model, next_purity, -chosen_var)
        return self.run_dpll(next_model, next_purity, depth + 1)

    def get_rand_unassigned(self, model):
        vars = range(1, self.num_vars + 1)
        unassigned = []
        for var in vars:
            if var not in model and -var not in model:
                unassigned.append(var)
        if unassigned:
            return random.choice(unassigned)
        return None

    def check_purities(self, model, purity_dict, chosen_var):
        clauses = []
        for clause in self.constraint_list:
            for var in clause:
                if var == chosen_var:
                    clauses.append(clause)
        for clause in clauses:
            for var in clause:
                purity_dict[var] -= 1
                if purity_dict[var] == 0:
                    if var not in model:
                        model.add(-var)

    # Gets unit clauses
    def get_unit_clauses(self, model):
        unit_list = []
        clause_list = []
        for clause in self.constraint_list:
            unit = None
            unit_exists = False
            for var in clause:
                if -var in model: # This var is false, keep checking
                    continue
                if var in model: # Some var is true
                    break
                # Else this var is unknown - if it's the first one, yay
                if not unit_exists:
                    unit_exists = True
                    unit = var
                else:
                    unit = None
            if unit_exists and unit is not None:
                unit_list.append(unit)
                clause_list.append(clause)
        if unit_list:
            return (unit_list, clause_list)
        return (None, None)


    # Checks if an assignment fulfils all constraints
    def is_valid(self, model):
        model_unknown = False
        for clause in self.constraint_list:
            valid = False
            clause_unknown = False
            for var in clause:
                if var in model: # clause is true
                    valid = True
                    break
                if -var in model: # this var of the constraint is false
                    continue

                clause_unknown = True # We don't know yeet

            if not valid and not clause_unknown:
                return 0 # False
            if clause_unknown:
                model_unknown = True

        if not model_unknown:
            return 1 # True

        return 2 # Unknown, not false

    def write_solution(self, sol_filename):
        sol_file = open(sol_filename, 'w')
        for val in self.model:
            if val > 0:
                #print("writing " + str(i + self.var_start))
                sol_file.write(str(self.var_map[val]))
                sol_file.write("\n")
                #print(self.var_map[val])
            else:
                #print("writing " + str(-i - self.var_start))
                sol_file.write(str(-self.var_map[-val]))
                sol_file.write("\n")
        #print(str(self.values))



#
