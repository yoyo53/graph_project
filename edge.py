class Edge:
    """An edge of a graph, composed of a source vertex, a target vertex, a weight and the graph it belongs to"""

    def __init__(self, graph, source, target, weight):
        """Create the edge given its source vertex, target vertex, weight and the graph it belongs to as parameter"""
        self.graph = graph
        self.source = source
        self.target = target
        self.weight = weight
