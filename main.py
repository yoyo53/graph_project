from graph import Graph
from interface import Interface
from os import listdir
from os.path import isfile


def make_traces_files():
    """Make the execution traces of all the test files"""
    for path in listdir("test files"):
        if isfile(f"test files/{path}") and path.endswith(".txt"):
            with open(f"execution traces/trace_{path}", "w") as file:
                file.write(Graph(f"test files/{path}").make_trace())


if __name__ == '__main__':
    graph = Graph('test files/test2.txt')
    print(graph.make_trace())
    interface = Interface()
    interface.mainloop()
