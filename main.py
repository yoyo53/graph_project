from graph import Graph
from interface import Interface

graph = Graph('test files/table 8.txt')
print(graph)
print(graph.as_formatted_matrix())
print(graph.get_earliest_date())
print(graph.get_latest_date())
print(graph.get_rank())


if __name__ == '__main__':
    interface = Interface()
    interface.run()

