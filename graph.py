from vertex import Vertex
from edge import Edge


class Graph:
    """A graph composed of a list of vertices and a list of edges"""

    def __init__(self, filepath):
        """Create a graph from a file, given the path of the file as parameter"""
        self.vertices = []
        self.edges = []
        self.filepath = filepath

        # open the file
        with open(filepath) as file:
            # read the lines of the file without blank lines and extra whitespaces at end of lines
            lines = file.readlines()
            lines = [line.replace("\n", "").strip(" ") for line in lines]
            lines = list(filter(None, lines))

            # Create one vertex for each task of the file, plus the two fictitious tasks 0 and N+1
            for i in range(0, len(lines) + 2):
                self.vertices.append(Vertex(self, str(i)))

            # loop through the lines of the file to create the edges corresponding to the constraints of each task
            for line in lines:
                line = line.split(" ")
                task = next(filter(lambda obj: obj.name == line[0], self.vertices))
                if len(line) == 2:
                    # if the task doesn't have any constraint, add an edge from the source (vertex 0) to this vertex
                    self.edges.append(Edge(self, self.vertices[0], task, 0))
                else:
                    # else, create an edge for each of the constraints of this task
                    for constraint in line[2:]:
                        source = next(filter(lambda obj: obj.name == constraint, self.vertices))
                        duration = next(filter(lambda line: line.split(" ")[0] == source.name, lines)).split(" ")[1]
                        self.edges.append(Edge(self, source, task, int(duration)))

            # loop through the vertices to find those who don't have successors and connect them to the target of the graph
            for vertex in self.vertices:
                if vertex != self.vertices[-1] and len(vertex.get_successors()) == 0:
                    duration = next(filter(lambda line: line.split(" ")[0] == vertex.name, lines), " 0").split(" ")[1]
                    self.edges.append(Edge(self, vertex, self.vertices[-1], int(duration)))

    def as_list(self):
        """Returns a string containing the number of vertices, number of edges and the list of edges of the graph"""
        lines = [f"{len(self.vertices)} vertices", f"{len(self.edges)} edges"]
        for edge in self.edges:
            lines.append(f'{edge.source.name} -> {edge.target.name} = {edge.weight}')
        return "\n".join(lines)

    def as_matrix(self):
        """Returns the adjacency matrix of the graph"""
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
        """Returns a string containing well formatted version of the adjacency matrix of the graph that can be directly displayed"""
        matrix = self.as_matrix()
        sizes = [max(map(len, col)) for col in zip(*matrix)]
        fmt = " | ".join(f"{{:{size}}}" for size in sizes)
        lines = [fmt.format(*row) for row in matrix]
        return "\n".join(lines)

    def is_scheduling(self):
        """Returns True if the graph satisfies the conditions to be a scheduling graph, and False otherwise"""
        sources = list(filter(lambda obj: len(obj.get_predecessors()) == 0, self.vertices))
        # if the graph has more than one source, return false as it's not a scheduling graph
        if len(sources) != 1:
            return False
        # if the edge leaving the source doesn't all have a 0 weight, return false as it's not a scheduling graph
        elif next(filter(lambda obj: obj.source == sources[0] and obj.weight != 0, self.edges), None) is not None:
            return False
        # if the graph has more than one target, return false as it's not a scheduling graph
        if len(list(filter(lambda obj: len(obj.get_successors()) == 0, self.vertices))) != 1:
            return False
        # if for any vertex, the edges leaving it doesn't all have the same weight, return false as it's not a scheduling graph
        for vertex in self.vertices:
            successors = vertex.get_successors()
            if len(successors) > 0 and next(filter(lambda obj: obj.weight != successors[0].weight, successors), None) is not None:
                return False
        # if there is an edge with negative weight, return false as it's not a scheduling graph
        if next(filter(lambda obj: obj.weight < 0, self.edges), None) is not None:
            return False
        # else return True as all conditions are satisfied
        return True

    def has_cycle(self):
        """Returns True if the contains at least one cycle, and False otherwise"""
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

    def get_rank(self):
        """Returns the list of the ranks of the vertices of the graph"""
        return [vertex.get_rank() for vertex in self.vertices]

    def get_earliest_date(self):
        """Returns the list of the earliest dates of the vertices of the graph"""
        return [vertex.get_earliest_date() for vertex in self.vertices]

    def get_latest_date(self):
        """Returns the list of the latest dates of the vertices of the graph"""
        return [vertex.get_latest_date() for vertex in self.vertices]

    def get_total_float(self):
        """Returns the list of the total floats of the vertices of the graph"""
        return [vertex.get_total_float() for vertex in self.vertices]

    def get_free_float(self):
        """Returns the list of the free floats of the vertices of the graph"""
        return [vertex.get_free_float() for vertex in self.vertices]

    def get_critical_path(self):
        """Returns the critical path(s) of this graph"""
        source = next(filter(lambda obj: len(obj.get_predecessors()) == 0, self.vertices))
        target = next(filter(lambda obj: len(obj.get_successors()) == 0, self.vertices))
        # initiate the critical path to the source of the graph
        paths = [[source]]
        # while all the critical paths doesn't ends at the target of the graph, continue to build them
        while next(filter(lambda obj: obj[-1] != target, paths), None) is not None:
            # loop through each critical paths to build them
            for path in paths:
                # get all the possibles vertices on which we can continue the current critical path
                successors = list(filter(lambda obj: obj.source == path[-1] and obj.target.get_total_float() == 0 and obj.source.get_earliest_date() + obj.weight == obj.target.get_earliest_date(), self.edges))
                if len(successors) > 0:
                    # if there are several results, duplicate the critical path for each result and continue to build each of them
                    for i in range(1, len(successors)):
                        paths.append(path + [successors[i].target])
                    # else just continue on a single critical path
                    path.append(successors[0].target)
        # when all the paths are complete, return the list of critical paths obtained
        return paths

    def make_trace(self):
        """Returns a string containing the execution trace corresponding to this graph by calling all the other functions"""
        trace = [f"graph from file {self.filepath.split('/')[-1]}", self.as_list(), self.as_formatted_matrix()]
        if not self.is_scheduling() or self.has_cycle():
            trace.append(
                "This is not a scheduling graph. A scheduling graph must satisfy the following conditions:\n"
                "    - a single entry point,\n"
                "    - a single exit point,\n"
                "    - no cycle,\n"
                "    - same weights for all outgoing edges of a vertex,\n"
                "    - outgoing edges of the entry vertex have zero,\n"
                "    - no negative edges.\n")
        else:
            trace.append("This is a scheduling graph with no cycle and no negative edges.")
            # put all the information about the vertices in the same matrix
            matrix = [["vertex"] + [vertex.name for vertex in self.vertices]]
            matrix += [["rank"] + [str(rank) for rank in self.get_rank()]]
            matrix += [["earliest date"] + [str(date) for date in self.get_earliest_date()]]
            matrix += [["latest date"] + [str(date) for date in self.get_latest_date()]]
            matrix += [["total float"] + [str(Float) for Float in self.get_total_float()]]
            matrix += [["free float"] + [str(Float) for Float in self.get_free_float()]]
            # format the matrix to be displayed more nicely
            sizes = [max(map(len, col)) for col in zip(*matrix)]
            fmt = " | ".join(f"{{:{size}}}" for size in sizes)
            trace += [fmt.format(*row) for row in matrix]
            critical_paths = self.get_critical_path()
            if len(critical_paths) > 1:
                trace.append("The critical paths are:")
            else:
                trace.append("The critical path is:")
            for path in self.get_critical_path():
                trace.append("    - " + " --> ".join(vertex.name for vertex in path))
        return "\n".join(trace)
