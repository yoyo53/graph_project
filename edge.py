class Edge:

    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __str__(self):
        return f'{self.source} -> {self.target} = {self.weight}'
