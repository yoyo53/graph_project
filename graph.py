from vertex import Vertex
from edge import Edge


class Graph:

    def __init__(self, filepath):
        self.vertices = []
        self.edges = []

        with open(filepath) as file:
            lines = file.readlines()
            lines = [line.replace("\n", "").strip(" ") for line in lines]
            lines = list(filter(None, lines))

            self.vertices.append(Vertex(self, "0"))
            for i in range(len(lines)):
                self.vertices.append(Vertex(self, str(i + 1)))
            self.vertices.append(Vertex(self, str(len(lines) + 1)))

            for line in lines:
                line = line.split(" ")
                task = next(filter(lambda obj: obj.name == line[0], self.vertices))
                if len(line) == 2:
                    self.edges.append(Edge(self, self.vertices[0], task, 0))
                else:
                    for constraint in line[2:]:
                        source = next(filter(lambda obj: obj.name == constraint, self.vertices))
                        duration = next(filter(lambda line: line.split(" ")[0] == source.name, lines)).split(" ")[1]
                        self.edges.append(Edge(self, source, task, int(duration)))

            for vertex in self.vertices:
                if vertex != self.vertices[-1] and len(vertex.get_successors()) == 0:
                    duration = next(filter(lambda line: line.split(" ")[0] == vertex.name, lines)).split(" ")[1]
                    self.edges.append(Edge(self, vertex, self.vertices[-1], int(duration)))

    def __str__(self):
        lines = [f"{len(self.vertices)} vertices", f"{len(self.edges)} edges"]
        for edge in self.edges:
            lines.append(str(edge))
        return "\n".join(lines)

    def as_matrix(self):
        matrix = [[""] + [vertex.name for vertex in self.vertices]]
        for source in self.vertices:
            matrix.append([source.name])
            for target in self.vertices:
                edge = next(filter(lambda obj: obj.source == source and obj.target == target, self.edges), None)
                if edge is None:
                    matrix[-1].append("*")
                else:
                    matrix[-1].append(str(edge.weight))
        return matrix

    def as_formatted_matrix(self):
        matrix = self.as_matrix()
        sizes = [max(map(len, col)) for col in zip(*matrix)]
        fmt = " | ".join(f"{{:{size}}}" for size in sizes)
        lines = [fmt.format(*row) for row in matrix]
        return "\n".join(lines)

    def is_scheduling(self):
        sources = list(filter(lambda obj: len(obj.get_predecessors()) == 0, self.vertices))
        if len(sources) != 1:
            return False
        elif next(filter(lambda obj: obj.source == sources[0] and obj.weight != 0, self.edges), None) is not None:
            return False
        if len(list(filter(lambda obj: len(obj.get_successors()) == 0, self.vertices))) != 1:
            return False
        for vertex in self.vertices:
            successors = vertex.get_successors()
            if len(successors) > 0 and next(filter(lambda obj: obj.weight != successors[0].weight, successors), None) is not None:
                return False
        if next(filter(lambda obj: obj.weight < 0, self.edges), None) is not None:
            return False
        return True

    def get_latest_date(self):
        return [vertex.get_latest_date() for vertex in self.vertices]

    def get_earliest_date(self):
        return [vertex.get_earliest_date() for vertex in self.vertices]

    def get_rank(self):
        return [vertex.get_rank() for vertex in self.vertices]

    def get_total_float(self):
        return [vertex.get_total_float() for vertex in self.vertices]

    def get_free_float(self):
        return [vertex.get_free_float() for vertex in self.vertices]

    def get_critical_path(self):
        source = next(filter(lambda obj: len(obj.get_predecessors()) == 0, self.vertices))
        target = next(filter(lambda obj: len(obj.get_successors()) == 0, self.vertices))
        paths = [[source]]
        while next(filter(lambda obj: obj[-1] != target, paths), None) is not None:
            for path in paths:
                successors = list(filter(lambda obj: obj.source == path[-1] and obj.target.get_total_float() == 0 and obj.source.get_earliest_date() + obj.weight == obj.target.get_earliest_date(), self.edges))
                if len(successors) > 0:
                    for i in range(1, len(successors)):
                        paths.append(path + [successors[i].target])
                    path.append(successors[0].target)
        return paths

    def has_cycle(self):
        nb_vertices = len(self.vertices)
        transitive_closure = [[0] * nb_vertices for _ in range(nb_vertices)]
        for edge in self.edges:
            transitive_closure[self.vertices.index(edge.source)][self.vertices.index(edge.target)] = 1
        for k in range(nb_vertices):
            for i in range(nb_vertices):
                for j in range(nb_vertices):
                    transitive_closure[i][j] |= (transitive_closure[i][k] and transitive_closure[k][j])
                    if transitive_closure[i][i]:
                        return True
        return False
