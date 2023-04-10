class Vertex:

    def __init__(self, graph, name):
        self.graph = graph
        self.name = name

    def get_predecessors(self):
        return list(filter(lambda obj: obj.target == self, self.graph.edges))

    def get_successors(self):
        return list(filter(lambda obj: obj.source == self, self.graph.edges))

    def get_earliest_date(self):
        predecessors = self.get_predecessors()
        if len(predecessors) == 0:
            return 0
        else:
            return max(edge.source.get_earliest_date() + edge.weight for edge in predecessors)

    def get_latest_date(self):
        successors = self.get_successors()
        if len(successors) == 0:
            return self.get_earliest_date()
        else:
            return min(edge.target.get_latest_date() - edge.weight for edge in successors)

    def get_rank(self):
        predecessors = self.get_predecessors()
        if len(predecessors) == 0:
            return 0
        else:
            return max(edge.source.get_rank() + 1 for edge in predecessors)

    def get_total_float(self):
        return self.get_latest_date() - self.get_earliest_date()

    def get_free_float(self):
        successors = self.get_successors()
        if len(successors) == 0:
            return 0
        else:
            min_date = min(successor.target.get_earliest_date() - successor.weight for successor in successors)
            return min_date - (self.get_earliest_date())
