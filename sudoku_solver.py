
import math
import random


class Solver:

    def __init__(self, sudoku: list[list[int]]) -> None:
        self.sudoku = [line[:] for line in sudoku]
        self.unsolved_sudoku = [line[:] for line in sudoku]
        self.box_size = int(len(sudoku)**0.5)



    def posible_values (self, int_row:int,int_column:int):
        row = set(self.sudoku[int_row])
        column = set([r[int_column] for r in self.sudoku])

        start_row = self.box_size* (int_row//self.box_size)
        start_column = self.box_size* (int_column//self.box_size)
        
        box = set()
        for r in range(start_row, start_row + self.box_size):
            for c in range(start_column, start_column + self.box_size):
                box.add(self.sudoku[r][c])
        
        all_digits = row.union(column).union(box) -set([0])
        return (set(range(1,len(self.sudoku)+1))-all_digits)
    
    def empty_cells(self):
        empty_cell = []
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku)):
                if self.sudoku[i][j] == 0:
                    empty_cell.append([i,j])
        
        return empty_cell


    def solve_sudoku(self):
        self.sudoku = [line[:] for line in self.unsolved_sudoku]
        memory = []
        empty_cell = self.empty_cells()
        i = 0
        while i< len(empty_cell):
            x,y = empty_cell[i]
            pos_values = list(self.posible_values(x,y))
            #pos_values.sort(reverse=True)
            random.shuffle(pos_values)
            
            if len(pos_values) == 0: # Si no hay soluciones, nos regresamos uno
                if not memory: return False # Si no hay donde regresar, no hay soluciones
                self.sudoku,pos_values,i = memory.pop() #Regresamos y continuamos
                x,y = empty_cell[i]
            self.sudoku[x][y] = pos_values.pop()

            if pos_values:
                memory.append([[line[:] for line in self.sudoku],pos_values,i])
                
            i+=1
        return True 

    

    def find_all_solutions(self):
        self.sudoku = [line[:] for line in self.unsolved_sudoku]
        solutions_count = 0
        memory = []
        empty_cell = self.empty_cells()
        i = 0
        x,y = [0,0]
        pos_values = list(self.posible_values(x,y))
        while True:
            if i < len(empty_cell):
                x,y = empty_cell[i]
                pos_values = list(self.posible_values(x,y))
                random.shuffle(pos_values)
            if i== len(empty_cell) or len(pos_values) == 0: # Si hay una solución, la contamos y regresamos
                if i == len(empty_cell): 
                    solutions_count+=1
                if not memory: return solutions_count # Si no hay donde regresar, encontramos todas.
                    
                self.sudoku,pos_values,i = memory.pop()
                x,y = empty_cell[i]
                
            self.sudoku[x][y] = pos_values.pop()
            if len(pos_values) >0:
                memory.append([[line[:] for line in self.sudoku],pos_values,i])
                
            
            i+=1

            

