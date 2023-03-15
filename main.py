from graph import Graph

graph = Graph('test files/test.txt')
print(graph)
print(graph.as_matrix())
print(graph.vertices[0].get_predecessors())