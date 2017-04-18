"""Implementation of Christofides Algorithm."""
import sys

from Generate import Edge
from Christofides import christofides

def christofides_alg(graph):
    vertices = graph.vertices
    size = len(vertices)
    distance_matrix = [[0 for n in range(size)] for m in range(size)]
    for x in range(size):
        for y in range(x+1, size):
            distance_matrix[x][y] = graph.distance(vertices[x], vertices[y])
    result = christofides.compute(distance_matrix)
    solution = result['Christofides_Solution']
    path = []
    for index in range(1, len(solution)):
        path = path + [Edge(solution[index - 1], solution[index])]
    return path