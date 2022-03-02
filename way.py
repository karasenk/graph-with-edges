import math


class Board:
    def __init__(self, edges, start, finish):
        self.edges = edges
        self.start = start
        self.finish = finish
        self.board = [[math.inf for _ in range(5)] for __ in range(7)]
        self.visited = []
        self.graph = [[math.inf for _ in range(5)] for __ in range(7)]  # для каждой вершины из какой вершины в неё пришли

    def get_value(self, coord0, coord1):
        for e in self.edges:
            if (e[0] == coord0 and e[1] == coord1) or \
               (e[0] == coord1 and e[1] == coord0):
                return e[2]
        return 1

    def mark(self, coords, n, coord0):
        for coord in coords:
            x, y = coord
            weight = self.get_value(coord, coord0)
            if self.board[x][y] > n + weight:
                self.board[x][y] = n + weight
                self.graph[x][y] = coord0

    def walk(self, coord0, x, y, n):
        self.board[x][y] = n
        # self.graph[x][y] = coord0
        self.visited.append((x, y))
        for row in self.visited:
            if math.inf in row:
                return True
        v = []
        if x - 1 >= 0 and (x - 1, y) not in self.visited:
            v.append((x - 1, y))
        if x + 1 < 7 and (x + 1, y) not in self.visited:
            v.append((x + 1, y))
        if y - 1 >= 0 and (x, y - 1) not in self.visited:
            v.append((x, y - 1))
        if y + 1 < 5 and (x, y + 1) not in self.visited:
            v.append((x, y + 1))
        if v:
            self.mark(v, n, (x, y))
            next_point = min(v, key=lambda a: self.board[a[0]][a[1]])
            n += self.get_value((x, y), next_point)
            return self.walk((x, y), next_point[0], next_point[1], n)
        return True

    def get_way(self, x, y, way):
        if self.start == (x, y) or not isinstance(self.graph[x][y], tuple):
            return way
        way.append(self.graph[x][y])
        x1, y1 = self.graph[x][y]
        return self.get_way(x1, y1, way)


    # это - функция, которую, получается, нужно импортировать в код с движением.
    # принимает список рёбер с их весом, координату старта, координату финиша.
    # принимает координаты у которых отсчёт начинается с 1 (н-р не (0, 0), а (1, 1))
    # возвращает путь в виде списка координат (н-р [(1, 2), (1,   3), (1, 4)]) (отсчёт тоже с 1)
def shortest_way(edges0, start, finish):
    start = start[0] - 1, start[1] - 1
    finish = finish[0] - 1, finish[1] - 1
    edges = []
    for coord in edges0:
        a = int(coord[0][0]) - 1, int(coord[0][1]) - 1
        b = int(coord[1][0]) - 1, int(coord[1][1]) - 1
        edges.append([a, b, int(coord[2])])
    board = Board(edges, start, finish)
    x, y = board.start
    board.walk((x, y), x, y, 0)
    for g in board.graph:
        print(g)
    x1, y1 = board.finish
    way = board.get_way(x1, y1, [(x1, y1)])
    return [(coord[0] + 1, coord[1] + 1) for coord in way][::-1]
