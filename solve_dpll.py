from display import display_sudoku_solution
import random, sys
from DPLL import DPLL

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    #random.seed(2)
    seed = 2
    random.seed(seed)
    thresh = .7
    #seed 8 thresh .6? puzz 1 - a mil iterations w no luck
    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    dpll = DPLL(sys.argv[1], 729, var_start=110)
    print("Seed: " + str(seed))
    result = dpll.init_dpll()
    print("Seed: " + str(seed))
    if result:
        dpll.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("Oh no bb what is u doin'")
