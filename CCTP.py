from Generate import Graph
from christofides import christofides_alg
import copy
from sets import Set

def cyclic_routing(graph):
	tour = christofides_alg(graph)
	edges = graph.all_edges
	vertices = [None, copy.deepcopy(graph.vertices)]
	path = []
	s = 0
	m = 1
	vertices[m].remove(graph.vertices[s])
	p = [0]
	direction = True
	while len(vertices[m]) > 1:
		shortcut_path = []
		for i in range(len(vertices[m])):
			shortcut_path.append(vertices[m][i])
		p.append(shortcut_path)
		print("M " + str(m))
		print(vertices[m])
		print(path)
		if m == 1 or vertices[m][0] == vertices[m-1][len(vertices[m-1]) - 1]:
			path = shortcut(direction, m, vertices, edges, path, graph.vertices)
			if vertices[m+1] == vertices[m]:
				#if nothing happened
				path = shortcut(not direction, m, vertices, edges, path, graph.vertices)
		else:
			direction = not direction
			path = shortcut(direction, m, vertices, edges, path, graph.vertices)
		m += 1
	print(p)
	return path

def shortcut(direction, m, vertices, edges, path, all_vertices):
	#foreward direction is true, backwards is false
	if not direction:
		vertices[m] = vertices[m][::-1]
	i = 0
	j = 1
	e = Set()
	vertices.append(copy.deepcopy(vertices[m]))
	while j < len(vertices[m]):
		if edges[_get_index(vertices[m][j], all_vertices)][_get_index(vertices[m][i], all_vertices)]:
			vertices[m+1].remove(vertices[m][j])
			path = path + [(_get_index(vertices[m][i], all_vertices), _get_index(vertices[m][j], all_vertices))]
			i = j
			j = i + 1
		else:
			e.add(((_get_index(vertices[m][j], all_vertices), _get_index(vertices[m][i], all_vertices))))
			l = _get_index(vertices[m][i], all_vertices) + 1
			while all_vertices[l] != vertices[m][j] \
				and (not edges[l][_get_index(vertices[m][i], all_vertices)]\
					or not edges[_get_index(vertices[m][j], all_vertices)][l]):
				if not edges[l][_get_index(vertices[m][i], all_vertices)]:
					e.add(l, _get_index(vertices[m][i], all_vertices))
				if not edges[_get_index(vertices[m][j], all_vertices)][l]:
					e.add(_get_index(vertices[m][j], all_vertices), l)
				l = l + 1
			if all_vertices[l] == vertices[m][j]:
				vertices[m+1].remove(vertices[m][j])
				print(l)
				path = path + [(_get_index(vertices[m][i], all_vertices), l), (l, _get_index(vertices[m][j], all_vertices))]
				i = j
				j = i + 1
			else:
				j = j + 1
	return path

def _get_index(vertex, all_vertices):
	return all_vertices.index(vertex)