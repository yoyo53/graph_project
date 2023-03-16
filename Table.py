from tkinter import *


class Table:

    def __init__(self, root, lst):
        self.row = len(lst)
        self.col = len(lst[0])
        self.mat = lst
        self.root = root

    def tktable(self, root):
        sizes = max([max(map(len, col)) for col in zip(*self.mat)])
        for i in range(self.row):
            for j in range(self.col):
                if i != 0 and j != 0 and self.mat[i][j] != "*":
                    self.e = Entry(self.root, width=sizes+5, fg='blue', font=('Arial', 16), justify="center")
                else:
                    self.e = Entry(self.root, width=sizes+5, fg='black', font=('Arial', 16), justify="center")

                self.e.grid(row=i, column=j)
                self.e.insert(0, self.mat[i][j])

