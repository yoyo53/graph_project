from graph import Graph
from Table import Table
from tkinter import *

graph = Graph('test files/table 8.txt')
print(graph)
print(graph.as_matrix())
print(graph.get_earliest_date())
print(graph.get_latest_date())
print(graph.get_rank())


# take the data

# find total number of rows and columns in list
# create root window
if __name__ == '__main__':
    root = Tk()
    root.state("zoomed")
    Table(root, graph.as_matrix())
    root.mainloop()

