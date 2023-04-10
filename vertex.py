class Vertex:
    """A vertex of a graph composed of its name and the graph it belongs to"""

    def __init__(self, graph, name):
        """Create the vertex name and the graph it belongs to as parameter"""
        self.graph = graph
        self.name = name

    def get_predecessors(self):
        """Returns the list of edges arriving to the vertex"""
        return list(filter(lambda obj: obj.target == self, self.graph.edges))

    def get_successors(self):
        """Returns the list of edges leaving the vertex"""
        return list(filter(lambda obj: obj.source == self, self.graph.edges))

    def get_rank(self):
        """Returns the rank of the vertex"""
        predecessors = self.get_predecessors()
        if len(predecessors) == 0:
            # if the vertex is a source of the graph, its rank is 0
            return 0
        else:
            # else we compute it recursively based on the ranks of the predecessors of the vertex
            return max(edge.source.get_rank() + 1 for edge in predecessors)

    def get_earliest_date(self):
        """Returns the earliest date of the vertex"""
        predecessors = self.get_predecessors()
        if len(predecessors) == 0:
            # if the vertex is a source of the graph, its earliest date is 0
            return 0
        else:
            # else we compute it recursively based on the earliest dates of the predecessors of the vertex
            return max(edge.source.get_earliest_date() + edge.weight for edge in predecessors)

    def get_latest_date(self):
        """Returns the latest date of the vertex"""
        successors = self.get_successors()
        if len(successors) == 0:
            # if the vertex is a target of the graph, its latest date is equal to its earliest date
            return self.get_earliest_date()
        else:
            # else we compute it recursively based on the latest dates of the successors of the vertex
            return min(edge.target.get_latest_date() - edge.weight for edge in successors)

    def get_total_float(self):
        """Returns the total float of a vertex by difference between its latest and earliest dates"""
        return self.get_latest_date() - self.get_earliest_date()

    def get_free_float(self):
        """Returns the free float of a vertex"""
        successors = self.get_successors()
        if len(successors) == 0:
            # if the vertex is a target of the graph, its free float is 0
            return 0
        else:
            # else we compute it based on the earliest dates of the successors of the vertex and its own earliest date
            min_date = min(successor.target.get_earliest_date() - successor.weight for successor in successors)
            return min_date - (self.get_earliest_date())
