from Generate import Edge
import copy
from Traversal import Traversal

class CCTP(Traversal):
    def __init__(self, graph, route):
        Traversal.__init__(self, graph)
        self.route = route
        self.num_brute = 0.0

    def compute(self):
        direction = True
        m = 1
        to_visit = [set()]
        best_path = [[]]
        tour = [self.current_node]
        for point in self.route[1:]:
            tour.append(point.a)
            to_visit[0].add(point.a)

        to_visit.append(copy.deepcopy(to_visit[0]))

        while len(to_visit[m]):
            best_path.append([])
            start_index = tour.index(self.current_node)
            best_path[m].append(self.current_node)
            for point in tour[start_index:] + tour[:start_index]:
                if point in to_visit[m]:
                    best_path[m].append(point)

            if m == 1 or best_path[m][0] == best_path[m - 1][len(to_visit[m - 1])]:
                self.shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m)
                if len(to_visit[m + 1]) == len(to_visit[m]):
                    self.shortcut(not direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m)
                    if len(to_visit[m + 1]) == len(to_visit[m]):
                        target = 1
                        while best_path[m][target] not in self.seen:
                            target = target + 1
                        self.go_to_closest_unvisted(to_visit[m])
                        to_visit[m+1].remove(self.current_node)
                        self.num_brute = self.num_brute + 1
                        self.look_around()
            else:
                direction = not direction
                self.shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m)
                if len(to_visit[m + 1]) == len(to_visit[m]):
                    target = 1
                    while best_path[m][target] not in self.seen:
                        target = target + 1
                    self.go_to_closest_unvisted(to_visit[m])
                    to_visit[m + 1].remove(self.current_node)
                    self.num_brute = self.num_brute + 1
                self.look_around()
            m = m + 1

        self.go_to_closest_unvisted({0})

    def shortcut(self, direction, best_path, _full_path, to_visit, m):
        if len(to_visit) == m + 1:
            to_visit.append(copy.deepcopy(to_visit[m]))
        if not direction:
            best_path = [best_path[0]] + best_path[::-1][:-1]
            full_path = [_full_path[0]] + _full_path[::-1][:-1]
        else:
            full_path = _full_path

        i = 0
        j = 1
        while j < len(best_path):
            vi = best_path[i]
            vj = best_path[j]
            min_ij = min(vi, vj)
            max_ij = max(vi, vj)
            if self.edges[max_ij][min_ij]:
                to_visit[m + 1].remove(vj)
                self.path += [Edge(vi, vj)]
                self.current_node = vj
                self.look_around()
                i = j
                j = j + 1
            else:
                l = full_path.index(best_path[i]) + 1
                vl = full_path[l]
                min_li = min(vl, vi)
                max_li = max(vl, vi)
                min_lj = min(vl, vj)
                max_lj = max(vl, vj)
                while vl != vj and (not self.edges[max_li][min_li] or not self.edges[max_lj][min_lj]):
                    l = l + 1
                    vl = full_path[l]
                    min_li = min(vl, vi)
                    max_li = max(vl, vi)
                    min_lj = min(vl, vj)
                    max_lj = max(vl, vj)
                if vl != vj:
                    to_visit[m + 1].remove(vj)
                    self.path += [Edge(vi, vl), Edge(vl, vj)]
                    self.current_node = vj
                    self.look_around()
                    i = j
                    j = j + 1
                else:
                    j = j + 1
