from vertex import Vertex
from edge import Edge


class Graph:

    def __init__(self, filepath):
        self.vertices = []
        self.edges = []
        self.is_directed = True

        with open(filepath) as file:
            lines = file.readlines()
            lines = [line.replace('\n', '') for line in lines]
            lines = list(filter(None, lines))

            for i in range(len(lines) + 2):
                self.vertices.append(Vertex(str(i)))

            for line in lines:
                line = line.split(" ")
                source = next(filter(lambda vertex: vertex.name == line[0], self.vertices))
                for target in line[2:]:
                    target = next(filter(lambda vertex: vertex.name == target, self.vertices))
                    self.edges.append(Edge(source, target, line[1]))

    def __str__(self):
        lines = [f'{len(self.vertices)} vertices', f'{len(self.edges)} edges']
        for edge in self.edges:
            lines.append(str(edge))
        return '\n'.join(lines)
