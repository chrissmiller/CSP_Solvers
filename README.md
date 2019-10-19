# Sudoku Assignment
Chris Miller '20
## GSAT
The GSAT algorithm loops up to iteration_lim number of loops. At each loop, it checks the validity of the current model using `is_valid()`, looping through every constraint and returning false if any constraint is false.

It then generates a random float in the range [0,1) and compares it to the given threshold, which defaults to .7. If the number is above the threshold, the algorithm picks a random value and flips it, which is a step used to escape local minima in the state space.

If the number is below or equal to the threshold, it generates a list of best flips - for every variable, it checks how many clauses would be satisfied if that variable was flipped, and returns the variable which would satisfy the most clauses (choosing a random one in the event of a tie.

This is implemented via the `get_best_flip` function, which flips each variable, scores the assignment, and unflips the variable, adding a tuple of the negative of the score and the variable to a min priority queue, then popping variables until the score changes to get the list of best flips. It then returns a random sample from the list to flip. 

GSAT was effective up to Rows.cnf, but was too slow to fulfil anything beyond that due to checking every variable's flip value at every iteration if a random variable is not chosen.


## WalkSAT
The WalkSAT algorithm follows a similar approach to GSAT, but instead of acting across the entire set of values, picks a random invalid clause using `get_invalid_clause()` (simultaneously checking for assignment validity). 

In WalkSAT, if the random value is over the threshold, the algorithm chooses a random value from the clause and flips it, and if not, it generates the best flips over the clause variables, allowing it to only evaluate two to nine flips instead of over seven hundred. This is where the primary speed of the algorithm comes from.

Both algorithms report progress (in # of constraints fulfilled) every 100 iterations.


## Testing
Use solve_sudoku.py and solve_dpll.py to test algorithms 

GSAT managed to solve one cell and all cells extremely quickly, and the rows constraint with around 600 iterations. As the prints show, the rate of constraint fulfillment drops dramatically as testing progresses, which is why more complex puzzles were impossible for the algorithm to solve in a reasonable timeframe.

(Seed 8, Threshold .7)

	Christophers-MacBook-Pro-5:hw5 chris$ python3 solve_sudoku.py rows.cnf
	At iteration 0, with 2360 constraints fulfilled out of 3078
	At iteration 100, with 2665 constraints fulfilled out of 3078
	At iteration 200, with 2861 constraints fulfilled out of 3078
	At iteration 300, with 2968 constraints fulfilled out of 3078
	At iteration 400, with 3038 constraints fulfilled out of 3078
	At iteration 500, with 3068 constraints fulfilled out of 3078
	At iteration 600, with 3075 constraints fulfilled out of 3078
	6 9 5 | 7 1 2 | 4 3 8 
	8 5 3 | 6 2 1 | 4 9 7 
	7 8 2 | 5 3 1 | 9 4 6 
	---------------------
	7 3 5 | 9 8 2 | 4 6 1 
	8 5 2 | 7 9 1 | 3 4 6 
	3 4 7 | 1 2 5 | 6 8 9 
	---------------------
	5 1 3 | 6 8 7 | 2 9 4 
	5 7 8 | 3 2 1 | 4 9 6 
	5 4 2 | 6 1 9 | 3 7 8  


Walksat, rows and cols:
(Seed 2, Threshold .7)

	At iteration 11300, with 3157 constraints fulfilled out of 3159
	5 8 1 | 9 4 6 | 7 3 2 
	9 2 5 | 8 1 3 | 6 4 7 
	6 4 9 | 5 7 8 | 2 1 3 
	---------------------
	4 3 2 | 1 8 7 | 5 9 6 
	1 5 7 | 6 2 4 | 3 8 9 
	2 1 6 | 3 5 9 | 4 7 8 
	---------------------
	7 9 8 | 2 3 5 | 1 6 4 
	3 6 4 | 7 9 2 | 8 5 1 
	8 7 3 | 4 6 1 | 9 2 5 



Walksat, puzzle 1:
	Seed: 2 Threshold: .7
	
	At iteration 70800, with 3248 constraints fulfilled out of 3250
	5 9 6 | 1 7 3 | 8 2 4 
	2 7 4 | 6 9 8 | 3 5 1 
	1 3 8 | 4 2 5 | 9 6 7 
	---------------------
	8 2 5 | 9 6 7 | 1 4 3 
	4 1 3 | 8 5 2 | 7 9 6 
	7 6 9 | 3 4 1 | 5 8 2 
	---------------------
	3 4 1 | 5 8 6 | 2 7 9 
	9 8 7 | 2 1 4 | 6 3 5 
	6 5 2 | 7 3 9 | 4 1 8 
	
With a different initialization (Seed 1, Threshold .7)

	At iteration 178300, with 3249 constraints fulfilled out of 3250
	5 3 6 | 2 8 4 | 1 9 7 
	1 7 4 | 5 9 6 | 3 2 8 
	9 2 8 | 1 3 7 | 5 6 4 
	---------------------
	8 5 2 | 7 6 1 | 9 4 3 
	4 9 3 | 8 5 2 | 7 1 6 
	7 6 1 | 9 4 3 | 8 5 2 
	---------------------
	6 4 9 | 3 7 5 | 2 8 1 
	2 8 7 | 4 1 9 | 6 3 5 
	3 1 5 | 6 2 8 | 4 7 9 
	
	
Clearly initializations and seeds are very important - Seed 8 threshold .6 led to over a million iterations on puzzle 1 with no solution, while other seeds converged in under a hundred thousand iterations.


## DPLL

I also implemented the Davis-Putnam-Logemann-Loveland algorithm for complete backtracking. This algorithm speeds up typical backtracking with a few heuristics, including checking purities and checking for unit clauses. 


Unit clauses are clauses in which either only one literal exists or all literals but one have been assigned false in the model. In either case, for the model to be true, the literal must evaluate to true, and we can simply assign the correct value (true for var, false for -var). 

Pure symbols are literals which are either true or are negated in every active clause (clauses which haven't yet been made true). IE, literal A is pure if in every constraint it appears as A or in every constraint it appears as -A. Thus by assigning A true (in the first case) or false (in the second case) we make every clause it appears in valid and do not cause any conflicts (since there are no cases in which that assignment causes a clause to not be true). 

	Christophers-MacBook-Pro-5:hw5 chris$ python3 solve_dpll.py all_cells.cnf
	Seed: 2
	Seed: 2
	8 4 7 | 2 1 1 | 4 5 6 
	6 6 4 | 9 1 7 | 4 1 1 
	8 1 1 | 4 3 1 | 2 9 2 
	---------------------
	4 2 3 | 2 6 6 | 3 7 4 
	1 5 5 | 1 5 6 | 2 3 1 
	9 5 9 | 7 8 2 | 1 3 6 
	---------------------
	7 4 4 | 4 8 1 | 1 1 6 
	6 3 5 | 4 8 4 | 9 8 9 
	2 6 1 | 9 2 9 | 1 2 7 
	
DPLL solves all_cells fairly quickly, but my implementation is too slow to implement effectively on a full puzzle. Efficiency improvements (and memory improvements via holding delete information instead of memory and computation heavy set and dictionary copies at every run) are likely to make the algorithm perform significantly better on larger, more useful problems. This is important because of the main advantage of DPLL - showing when a problem is unsolveable.

I implemented unit clause checking by exhaustively searching for clauses with all but one unit being False, and chose to implement purity checking implicitly. As clauses were satisfied, all variables in them had a counter for number of appearances as positive and negative. If a counter for either one hit zero and the variable was not already set in the model, it was added to the model in the way which fulfilled all clauses it was needed in.

## SATLim
In SATLim, I tracked a set of constant variables, and ensured that a variable was not preset (for example, the variables which appear alone in clauses and thus have unchangeable values) when flipping variables. This did seem to have minor performance improvements, and on average over the first fifty to a hundred thousand iterations a flip 'hit,' or tried to violate this constraint, every three and a half iterations for puzzle 1. This meant that the change frequently blocked changes which would have checked assignments which were invalid from the start. 

Checking is valuable, since otherwise the algorithm may appear to be almost complete (for example, fulfilling all but one constraint) but may in reality be miles from a correct solution if the one violated constraint is one which flipping breaks dozens or even hundreds of others. This is clearly the case with Sudoku - by ignoring 5 to 20 preset "clue" constraints and fulfilling all others, the algorithm may create a valid board which fulfils none of the actual sudoku clues and is thus likely to be very far from the correct solution. 

