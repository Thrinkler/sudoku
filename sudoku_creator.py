import random
from sudoku_solver import Solver
class Creator:
    
    def __init__(self, size = 3) -> None:
        self.size = size**2
    

    def new_sudoku_ending(self):
        s = Solver([[0 for _ in range(self.size)]for _ in range(self.size)])
        s.solve_sudoku()
        return s.sudoku

    def ret_sudoku(self):
        return [[0,0,6,0,0,7,0,2,0],
                [2,0,0,0,4,8,0,0,0],
                [4,1,0,0,0,3,0,0,0],
                [0,0,0,0,5,0,4,8,0],
                [0,4,8,0,0,0,9,7,0],
                [0,9,2,0,6,0,0,0,0],
                [0,0,0,4,0,0,0,6,3],
                [0,0,0,9,1,0,0,0,8],
                [0,5,0,3,0,0,1,0,0],]

    def print_sudoku(self, sudoku):
        for line in sudoku:
            print(line)


    def create_sudoku(self, max_clues=17):
        sudoku = self.new_sudoku_ending()

        clues = len(sudoku)* len(sudoku[0])
        pos_clues = [[[x,y] for x in range(0,len(sudoku))]for y in range(0,len(sudoku))]

        p_clues = []
        not_watched_clues = []
        for line in pos_clues:
            p_clues += [i[:] for i in line]
            not_watched_clues += [i[:] for i in line]
        
        n =0

        while clues > max_clues:
            if len(not_watched_clues) == 0: #Si ya se probó quitar todos los números y hay más de una solución si los quitas
                return sudoku
            
            x,y = random.choice(not_watched_clues)
            removed_clue = sudoku[x][y]        
            sudoku[x][y] = 0

            s = Solver(sudoku)
            if(s.find_all_solutions() == 1):
                clues-=1
                p_clues.remove([x,y])
                not_watched_clues = [line[:] for line in p_clues]

            else:
                sudoku[x][y] = removed_clue
                not_watched_clues.remove([x,y])
            n+=1
            print(n, clues)
        return sudoku
    
    
    def create_min_sudoku(self, max_clues=17):
        sudoku = self.new_sudoku_ending()
        solved_sudoku = [line[:] for line in sudoku]

        clues = len(sudoku)* len(sudoku[0])
        pos_clues = [[[x,y] for x in range(0,len(sudoku))]for y in range(0,len(sudoku))]

        p_clues = []
        not_watched_clues = []
        for line in pos_clues:
            p_clues += [i[:] for i in line]
            not_watched_clues += [i[:] for i in line]
        n =0

        min_ret_sudoku = []

        has_not_complete_one = True

        while clues > max_clues and (n<500 or has_not_complete_one):

            if len(not_watched_clues) == 0: #Si ya se probó quitar todos los números y hay más de una solución si los quitas
                min_ret_sudoku = [line[:] for line in sudoku]
                has_not_complete_one = False
                a,b = random.randint(0,len(sudoku)-1),random.randint(0,len(sudoku)-1)

                for line in [[(a+i)%len(sudoku),(b+random.randint(0,len(sudoku)-1))%len(sudoku)] for i in range(len(sudoku))]:
                    if line not in p_clues:
                        p_clues.append(line)
                        sudoku[line[0]][line[1]] = solved_sudoku[line[0]][line[1]]
                        clues+=1
                not_watched_clues = [line[:] for line in p_clues]
                
            
            x,y = random.choice(not_watched_clues)
            removed_clue = sudoku[x][y]        
            sudoku[x][y] = 0

            s = Solver(sudoku)
            if(s.find_all_solutions() == 1):
                clues-=1
                p_clues.remove([x,y])
                not_watched_clues = [line[:] for line in p_clues]

            else:
                sudoku[x][y] = removed_clue
                not_watched_clues.remove([x,y])
            if n%5 == 0:
                print(n, clues)
            n+=1

        return min_ret_sudoku