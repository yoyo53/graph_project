from graph import Graph
from Table import Table
from tkinter import *
graph = Graph('test files/table 8.txt')
print(graph)
print(graph.as_matrix())
print(graph.get_earliest_dates())
print(graph.get_latest_date())
print(graph.get_rank())


# take the data

# find total number of rows and
# columns in list
# create root window
root = Tk()
lst = Table(root, graph.as_matrix())
t = lst.tktable(root)
lst.root.mainloop()

