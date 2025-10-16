from sudoku_creator import Creator
from sudoku_solver import Solver

def sudoku_test():
    sud = Creator().ret_sudoku()

    for line in sud:
        print(line)

    solver = Solver(sud)

    print()
    print("there are ",solver.find_all_solutions())
    #for line in solver.sudoku:
    #    print(line)
    #print()

    solver = Solver(sud)
    solver.solve_sudoku()

    for line in solver.sudoku:
        print(line)

def sudoku_creator():
    sud = Creator(4).create_sudoku()

    for line in sud:
        print(line)

    print()
    solver = Solver(sud)
    
    print("there are ",solver.find_all_solutions())

    solver = Solver(sud)
    solver.solve_sudoku()

    for line in solver.sudoku:
        print(line)

if __name__ == "__main__":
    sudoku_creator()

