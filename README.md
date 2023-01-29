# KenKen-Problem

Arithmetic and Logic puzzle\
Constraint satisfaction problem

KenKen and KenDoku are trademarked names for a style of arithmetic and logic puzzle invented in 2004 by Japanese math teacher Tetsuya Miyamoto, who intended the puzzles to be an instruction-free method of training the brain. The name derives from the Japanese word for cleverness (賢, ken, kashiko(i)). The names Calcudoku and Mathdoku are sometimes used by those who do not have the rights to use the KenKen or KenDoku trademarks.


• n^2 Variables (0 to n-1)\
• n^2 Domains (1 to n)\
• Cages : set with numbers and operators\
• Operator (5 vlaues):\
{ '+' : Addition,\
'-' : Subtraction,\
'*' : Multiplication,\
'/' : Division,\
'=' : None }\
• Neighbors : A list of every value (0 to n). Every value of the matrix holds all horizontal and vertical values, except that value\
• Constraints:
The value that we select should not be used both horizontally nor vertically. Also in the cage we should consider all the values and operators so as the cage to be correct.\

The algorithms that i compare with backtracking are :\
• mrv / fc\
• mrv / mac\
Results: As we run the problem, we can clearly see that mrv / fc is slower than mrv / mac and especially in hard problems and also mrv / mac makes more assigns than mrv / fc.

To run kenken problem type in terminal :\
$ python kenken.py
