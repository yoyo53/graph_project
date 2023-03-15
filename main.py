from graph import Graph

graph = Graph('test files/test.txt')
print(graph)
print(graph.as_matrix())
print(graph.get_earliest_dates())
print(graph.get_latest_date())