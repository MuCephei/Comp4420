"""Implementation of Christofides Algorithm."""
from Generate import Edge
from Christofides import christofides


def christofides_alg(graph):
    vertices = graph.vertices
    size = len(vertices)
    distance_matrix = [[0 for a in range(size)] for b in range(size)]
    print(vertices)
    print(distance_matrix)
    for x in range(size):
        for y in range(x+1, size):
            distance = graph.distance(vertices[x], vertices[y])
            print(distance)
            distance_matrix[x][y] = distance
            distance_matrix[y][x] = distance
    print(distance_matrix)
    result = christofides.compute(distance_matrix)
    solution = result['Christofides_Solution']
    path = []
    for index in range(1, len(solution)):
        path += [Edge(solution[index - 1], solution[index])]
    return path
