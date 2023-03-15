class Vertex:

    def __init__(self, graph, name):
        self.graph = graph
        self.name = name

    def __str__(self):
        return self.name

    def get_predecessors(self):
        edges = filter(lambda obj: obj.target == self, self.graph.edges)
        return [edge.source for edge in edges]

    def get_successors(self):
        edges = filter(lambda obj: obj.source == self, self.graph.edges)
        return [edge.target for edge in edges]
