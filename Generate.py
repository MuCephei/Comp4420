import random
from sets import Set

class Graph:
	max_x = 100
	max_y = 100

	def __init__(self, number_of_vertices, number_to_remove):
		self.number_of_vertices = number_of_vertices
		self.number_of_broken_edges = number_to_remove

		self.vertices = [(random.random() * Graph.max_y, random.random() * Graph.max_x) for n in range(self.number_of_vertices)]
		self.all_edges = remove_edges(self.number_of_broken_edges, self.number_of_vertices)

	def __str__(self):
		print(self.vertices)
		print(self.all_edges)
		return ""

def is_edge_safe_to_remove(edge, edges, edges_as_matrix, size):
	if edges_as_matrix[edge[0]][edge[1]] == 1:
		vertices = Set()
		new_vertices = Set([0])
		newer_vertices = Set()
		edges_as_matrix[edge[0]][edge[1]] = 0
		while len(new_vertices) > 0:
			vertices = vertices.union(new_vertices)
			newer_vertices.clear()
			for v in new_vertices:
				for x in range(v):
					if x not in vertices and x not in newer_vertices:
						if edges_as_matrix[v][x] == 1:
							newer_vertices.add(x)
				for y in range(v,size):
					if y not in vertices and y not in newer_vertices:
						if edges_as_matrix[y][v] == 1:
							newer_vertices.add(y)
			new_vertices = newer_vertices.copy()
			newer_vertices.clear()

		edges_as_matrix[edge[0]][edge[1]] = 1
		return len(vertices) == size
	else:
		return False

def remove_edges(number_to_remove, number_of_vertices):
	all_edges = [(m,n) for m in range(number_of_vertices) for n in range(m)]
	edges_as_matrix = [[1 for n in range(m)] for m in range(number_of_vertices)]
	for removal in range(number_to_remove):
		edge = random.choice(all_edges)
		while not is_edge_safe_to_remove(edge, all_edges, edges_as_matrix, number_of_vertices):
			edge = random.choice(all_edges)
		all_edges.remove(edge)
		edges_as_matrix[edge[0]][edge[1]] = 0
	return edges_as_matrix

graph = Graph(5,6)
print(graph)