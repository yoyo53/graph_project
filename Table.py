from tkinter import *


class Table:
    def __init__(self, root, matrix):
        size = max([max(map(len, col)) for col in zip(*matrix)]) + 5
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != "*":
                    color = 'blue'
                else:
                    color = 'black'
                Label(root, width=size, fg=color, font=('Arial', 16), justify="center", text=matrix[i][j], relief=RAISED).grid(row=i, column=j)
