from vertex import Vertex
from edge import Edge


class Graph:

    def __init__(self, filepath):
        self.vertices = []
        self.edges = []
        self.is_directed = True

        with open(filepath) as file:
            lines = file.readlines()
            lines = [line.replace("\n", "").strip(" ") for line in lines]
            lines = list(filter(None, lines))

            source = Vertex("0")
            self.vertices.append(source)
            for i in range(1, len(lines) + 1):
                self.vertices.append(Vertex(str(i)))
            destination = Vertex(str(len(lines) + 1))
            self.vertices.append(destination)

            for line in lines:
                line = line.split(" ")
                task = next(filter(lambda obj: obj.name == line[0], self.vertices))
                if len(line) == 2:
                    self.edges.append(Edge(source, task, 0))
                else:
                    for constraint in line[2:]:
                        source = next(filter(lambda obj: obj.name == constraint, self.vertices))
                        duration = next(filter(lambda line: line.split(" ")[0] == source.name, lines)).split(" ")[1]
                        self.edges.append(Edge(source, task, int(duration)))

            for vertex in self.vertices:
                if vertex != destination and next(filter(lambda obj: obj.source == vertex, self.edges), None) is None:
                    duration = next(filter(lambda line: line.split(" ")[0] == vertex.name, lines)).split(" ")[1]
                    self.edges.append(Edge(vertex, destination, duration))

    def __str__(self):
        lines = [f'{len(self.vertices)} vertices', f'{len(self.edges)} edges']
        for edge in self.edges:
            lines.append(str(edge))
        return '\n'.join(lines)

    def as_matrix(self):
        matrix = [[""] + [vertex.name for vertex in self.vertices]]
        for source in self.vertices:
            matrix.append([source.name])
            for i in range(1, len(matrix[0])):
                destination = next(filter(lambda obj: obj.name == matrix[0][i], self.vertices))
                edge = next(filter(lambda obj: obj.source == source and obj.target == destination, self.edges), None)
                if edge is None:
                    matrix[-1].append("*")
                else:
                    matrix[-1].append(str(edge.weight))

        sizes = [max(map(len, col)) for col in zip(*matrix)]
        fmt = " | ".join(f"{{:{size}}}" for size in sizes)
        table = [fmt.format(*row) for row in matrix]
        return "\n".join(table)
