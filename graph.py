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
            for i in range(1, len(lines)):
                self.vertices.append(Vertex(str(i)))
            destination = Vertex(str(len(lines)))
            self.vertices.append(destination)

            for line in lines:
                line = line.split(" ")
                task = next(filter(lambda obj: obj.name == line[0], self.vertices))
                if len(line) == 2:
                    self.edges.append(Edge(source, task, 0))
                else:
                    for constraint in line[2:]:
                        target = next(filter(lambda obj: obj.name == constraint, self.vertices))
                        self.edges.append(Edge(task, target, int(line[1])))

            for vertex in self.vertices:
                if next(filter(lambda obj: obj.source == vertex, self.edges), None) is None:
                    duration = next(filter(lambda line: line.split(" ")[0] == vertex.name, lines)).split(" ")[1]
                    self.edges.append(Edge(vertex, destination, duration))

    def __str__(self):
        lines = [f'{len(self.vertices)} vertices', f'{len(self.edges)} edges']
        for edge in self.edges:
            lines.append(str(edge))
        return '\n'.join(lines)
