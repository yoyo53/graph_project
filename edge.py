class Edge:

    def __init__(self, graph, source, target, weight):
        self.graph = graph
        self.source = source
        self.target = target
        self.weight = weight

    def __str__(self):
        return f'{self.source} -> {self.target} = {self.weight}'
