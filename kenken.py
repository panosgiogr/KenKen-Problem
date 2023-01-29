# Author: Panagiotis Giovanos
#    SDI: 20******
# Lesson: Artificial Intelligence - YS02

from csp import *
import time
import operator

oper_dict = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '=': None }

class CAGE:
    def __init__(self, Variables, op, result):
        self.Variables = Variables
        self.op = op
        self.result = result
    def Solution(self, Temp_Var, Current_Value, Current_Domains):
        if len(Temp_Var) == 0: return Current_Value == self.result
        for value in Current_Domains[Temp_Var[0]]:
            if self.op == '+' or self.op == '*' and  self.Solution(Temp_Var[1:], oper_dict[self.op](value,Current_Value), Current_Domains) == True:
                return True
        return False

class kenken(CSP):
    def __init__(self, Input):
        Data = self.Parse_Data(Input)
        self.n = Data[0]
        self.Variables = [i for i in range(self.n * self.n)]
        self.Domains = {Temp_Var: [i + 1 for i in range(self.n)] for Temp_Var in self.Variables}
        self.Cages = []
        for i in range(len(Data[3])): self.Cages.append(CAGE(Data[3][i], Data[2][i], Data[1][i]))
        self.Neighbors = {Temp_Var: self.Columns(Temp_Var) + self.Rows(Temp_Var) for Temp_Var in self.Variables}
        for Temp_Var in self.Variables:
            for Temp_Cage in self.Cages:
                if Temp_Var in Temp_Cage.Variables:
                    Temp_Variables = list(Temp_Cage.Variables)
                    Temp_Variables.remove(Temp_Var)
                    self.Neighbors[Temp_Var] = self.Neighbors[Temp_Var] + Temp_Variables
        CSP.__init__(self, self.Variables, self.Domains, self.Neighbors, self.Contraints)
        self.Current_Domains = {v: list(self.Domains[v]) for v in self.Variables}
        for Temp_Var in self.Variables:
            self.Neighbors[Temp_Var] = list(dict.fromkeys(self.Neighbors[Temp_Var]))

    def Parse_Data(self, Input):
        Return_Numbers = []
        Return_Operators = []
        Return_Cages = []
        with open(Input, "r") as Contraints: Lines = [line.rstrip() for line in Contraints]
        Return_n = int(Lines[0])
        Lines.pop(0)
        for Line in Lines:
            t = Line.split('#', 1)[0]
            Return_Numbers.append(int(t))
            Line = Line[len(t):]
            Return_Operators.append(Line[len(Line) - 1])
            Line = Line[1:len(Line) - 2]
            Number = ''
            Cage_Tuple = ()
            for char in Line:
                if char != '-': Number = Number + char
                else:
                    Cage_Tuple = Cage_Tuple + (int(Number),)
                    Number = ''
            Cage_Tuple = Cage_Tuple + (int(Number),)
            Return_Cages.append(Cage_Tuple)
        return (Return_n, Return_Numbers, Return_Operators, Return_Cages)

    def Rows(self, Variable):
        for i in range(self.n):
            Return_Rows = self.Variables[i * self.n:(i + 1) * self.n]
            if (Variable in Return_Rows):
                Return_Rows.remove(Variable)
                return Return_Rows

    def Columns(self, Variable):
        for i in range(self.n):
            Return_Columns = []
            for j in range(0, self.n * self.n, self.n):
                Return_Columns.append(i + j)
            if (Variable in Return_Columns):
                Return_Columns.remove(Variable)
                return Return_Columns

    def Return_Cage(self, Temp_Var):
        for Temp_Cage in self.Cages:
            if Temp_Var in Temp_Cage.Variables:
                return Temp_Cage

    def Contraints(self, A, a, B, b):
        if (B in self.Columns(A) or B in self.Rows(A)) and a == b: return False
        A_Cage = self.Return_Cage(A)
        B_Cage = self.Return_Cage(B)
        A_Cage_Variables = list(A_Cage.Variables)
        B_Cage_Variables = list(B_Cage.Variables)
        if len(A_Cage_Variables) == 1 or len(B_Cage_Variables) == 1:
            return (a == A_Cage.result if len(A_Cage_Variables) == 1 else True and b == B_Cage.result if len(B_Cage_Variables) == 1 else True)
        if A_Cage == B_Cage:
            A_Cage_Variables.remove(A)
            A_Cage_Variables.remove(B)
            if A_Cage.op == '+' or A_Cage.op == '*':
                return A_Cage.Solution(A_Cage_Variables, oper_dict[A_Cage.op](a,b), self.Current_Domains)
            if A_Cage.op == '-' or A_Cage.op == '/':
                return (oper_dict[A_Cage.op](a,b) == A_Cage.result if A_Cage.op == '-' else oper_dict[A_Cage.op](a,b) == float(A_Cage.result)) or (oper_dict[A_Cage.op](b,a) == A_Cage.result if A_Cage.op == '-' else oper_dict[A_Cage.op](b,a) == float(A_Cage.result))
        return True

    def print_puzzle(self, puzzle):
        if puzzle == None:
            print("No solution found with this settings")
            return 0
        else:
            for i in range(self.n * self.n):
                if (i % (self.n) == 0): print("")
                if i in puzzle: print(str(puzzle[i]) + " ", end='')
                else: print("x ", end='')
            print("\n")
            return 1

def Problem_Solver(problems, algorithmn, select_unassigned_variable, inf = no_inference, Is_Min_Max = 0):
    solved = 0
    problems_list = []
    if Is_Min_Max: print("Minmax running")
    for i in range(len(problems)):
        start_problem = time.time()
        AC3(problems[i])
        print("Solving Problem p" + str(i) + " size " + str(problems[i].n) + "*" + str(problems[i].n))
        if Is_Min_Max:
            solved += problems[i].print_puzzle(min_conflicts(problems[i], 3000))
        else:
            solved += problems[i].print_puzzle(algorithmn(problems[i], select_unassigned_variable, inference = inf))
        print("Asssigns = " + str(problems[i].nassigns))
        end_problem = time.time()
        problems_list.append((end_problem - start_problem, problems[i].nassigns))
        print(end_problem - start_problem)
    print("Solved " + str(solved) + "/" + str(len(problems)))
    solved_times = 0
    for times in problems_list:
        solved_times += times[0]
    print("Cpu Time = " + str(solved_times) + " s")
    return problems_list

#Initialize problems
problems = [kenken("p/Kenkel-3-easy.txt"), kenken("p/Kenken-4-Hard.txt"), kenken("p/Kenken-5-Hard.txt"), kenken("p/Kenken-6-Hard.txt"),
            kenken("p/Kenken-7-Hard-1.txt"), kenken("p/Kenken-7-Hard-2.txt"), kenken("p/Kenken-8-Hard-1.txt"),  kenken("p/Kenken-8-Hard-2.txt"),
            kenken("p/Kenken-9-Hard-1.txt"),  kenken("p/Kenken-9-Hard-2.txt")]
problems_list = []
# run with forward_checking
problems_list.append(Problem_Solver(problems, backtracking_search, mrv, forward_checking))
# run with mac
problems_list.append(Problem_Solver(problems, backtracking_search, mrv, mac))
print("\nTime Table for all problems/algorithms")
print("    mrv/fc      mrv/mac")

Total_times = 0
Total_assigns = 0
for i in range(len(problems)):
    print("p" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(problems_list)):
        print(str('%.8f' % problems_list[j][i][0]) + "s ", end='')
        Total_times += problems_list[j][i][0]
    print("")
print("")
for i in range(len(problems)):
    print("p" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(problems_list)):
        print(str(problems_list[j][i][1]) + " assigns ", end='')
        Total_assigns += problems_list[j][i][1]
    print("")
print("Total CPU Time : " + str(Total_times) + "s ")
print("Total Assigns : " + str(Total_assigns) + " assigns ")