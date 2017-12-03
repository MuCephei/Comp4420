class Edge:
    """A connection from the vertex at index a, to the vertex at index b."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + " - " + str(self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash(self.__str__())

    __repr__ = __str__