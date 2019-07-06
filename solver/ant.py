from numpy import inf
import numpy.random as random

def edge_attraction(phi, dist, alpha, beta):
    """Вычисляет привлекательность ребра по формуле"""
    return phi ** alpha * (1 / dist) ** beta

class AntPath:
    class PathNode:
        def __init__(self, data=None, prev=None, next=None):
            self.d = data
            self.next = self if next is None else next
            self.prev = self if prev is None else prev
        
    def __init__(self, v):
        self.sent = AntPath.PathNode()
        self.sent.next = AntPath.PathNode(v, self.sent, self.sent)
        self.sent.prev = self.sent.next

    @property
    def start(self):
        return self.sent.next

    @property
    def end(self):
        return self.sent.prev

    def append(self, v):
        new = AntPath.PathNode(v, self.end, self.sent)
        self.end.next = new
        self.sent.prev = new
    
    def extract(self, start, end):
        start.prev.next = end.next
        end.next.prev = start.prev

    def clear(self):
        self.sent.prev = self.sent
        self.sent.next = self.sent


class Ant:
    """Класс, моделирующий поведение муравья"""
    def __init__(self, a, b, Q, G, pos):
        self.alpha = a
        self.beta = b
        self.Q = Q
        self.assoc_graph = G
        self.path = AntPath(pos)

    @property
    def pos(self):
        return self.path.end.d

    @pos.setter
    def pos(self, value):
        if not isinstance(value, tuple):
            raise TypeError("Передан не кортеж")
        if not len(value) == 3:
            raise ValueError("Значение не является точкой")
        if not self.assoc_graph.vert_in_graph(value):
            raise ValueError("Точка не принадлежит графу")
        self.path.append(value)

    @property
    def path_len(self):
        ret = 0.0
        n = self.path.start
        while n != self.path.end:
            ret += self.assoc_graph[n.d, n.next.d].weight
            n = n.next
        return ret

    def pick_edge(self):
        """Совершает перемещение в одну из соседних точек в графе G"""

        G = self.assoc_graph

        targets = list(G.get_adjacent(self.pos))
        edges = [G[self.pos, t] for t in targets]
        
        # привлекательности ребер
        attr = [edge_attraction(e.phi,
                                e.weight,
                                self.alpha,
                                self.beta)
                if e.weight != inf # inf значит ребра нет
                else 0.0
                for e in edges]
        
        total_attr = sum(attr)
        attr = [a / total_attr for a in attr]
        
        # случайный выбор тут
        choice = random.choice(len(edges), p=attr)
        
        # добавить в путь
        self.pos = targets[choice]

    def remove_cycles(self):
        """Извлекает циклы из пути"""
        cur_left = self.path.start
        while cur_left != self.path.end:
            cur_right = self.path.end
            while cur_right != cur_left:
                if cur_left.d == cur_right.d:
                    self.path.extract(cur_left.next, cur_right)
                    break
                cur_right = cur_right.prev
            cur_left = cur_left.next

    def distribute_pheromone(self):
        """Распространяет феромон по всем пройденным ребрам"""
        phi = self.Q / self.path_len
        
        n = self.path.start
        while n != self.path.end:
            self.assoc_graph[n.d,n.next.d].phi += phi
            n = n.next

    def unwind_path(self):
        """Возвращает муравья к начальному состоянию"""

        pos = self.path.start.d
        self.path.clear()
        self.path.append(pos)