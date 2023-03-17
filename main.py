from graph import Graph
from interface import Interface

graph = Graph('test files/test2.txt')
print(graph)
print(graph.as_formatted_matrix())
print(graph.get_earliest_date())
print(graph.get_latest_date())
print(graph.get_rank())
print(graph.get_total_float())
print(graph.get_free_float())
paths = graph.get_critical_path()
print("Critical paths:")
for path in paths:
    print("- " + " --> ".join(str(cell) for cell in path))

if __name__ == '__main__':
    interface = Interface()
    interface.mainloop()
