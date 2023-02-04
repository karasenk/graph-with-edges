import math


class Board:
    def __init__(self, edges, start, finish):
        self.edges = edges
        self.board = [[math.inf for _ in range(5)] for __ in range(7)]
        self.visited = []
        self.graph = [[math.inf for _ in range(5)] for __ in range(7)]  # для каждой вершины из какой вершины в неё пришли
        self.start = start
        self.finish = finish

    def get_value(self, coord0, coord1):
        for e in self.edges:
            if (e[0] == coord0 and e[1] == coord1) or \
               (e[0] == coord1 and e[1] == coord0):
                return e[2]
        return 1

    def mark(self, coord, n, coord0):
        x, y = coord
        weight = self.get_value(coord, coord0)
        if self.board[x][y] > n + weight:
            self.board[x][y] = n + weight
            self.graph[x][y] = coord0

    def walk(self, x, y, n=0):
        self.visited.append((x, y))
        if x - 1 >= 0 and (x - 1, y) not in self.visited:
            self.mark((x - 1, y), n, (x, y))
        if x + 1 < 7 and (x + 1, y) not in self.visited:
            self.mark((x + 1, y), n, (x, y))
        if y - 1 >= 0 and (x, y - 1) not in self.visited:
            self.mark((x, y - 1), n, (x, y))
        if y + 1 < 5 and (x, y + 1) not in self.visited:
            self.mark((x, y + 1), n, (x, y))
        values = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) not in self.visited:
                    values.append((i, j))
        if not values:
            return True
        x1, y1 = min(values, key=lambda w: self.board[w[0]][w[1]])
        n = self.board[x1][y1]
        return self.walk(x1, y1, n)

    def get_way(self, x, y, way):
        if self.start == (x, y) or not isinstance(self.graph[x][y], tuple):
            return way
        way.append(self.graph[x][y])
        x1, y1 = self.graph[x][y]
        return self.get_way(x1, y1, way)

    def calculate_finish(self):
        points = []
        x, y = self.finish
        if x - 2 >= 0:
            points.append(([(x - 1, y), (x - 2, y)],
                           self.get_value((x, y), (x - 1, y)) +
                           self.get_value((x - 1, y), (x - 2, y))))
        if x + 2 < 7:
            points.append(([(x + 1, y), (x + 2, y)],
                           self.get_value((x, y), (x + 1, y)) +
                           self.get_value((x + 1, y), (x + 2, y))))
        if y - 2 >= 0:
            points.append(([(x, y - 1), (x, y - 2)],
                           self.get_value((x, y), (x, y - 1)) +
                           self.get_value((x, y - 1), (x, y - 2))))
        if y + 2 < 5:
            points.append(([(x, y + 1), (x, y + 2)],
                           self.get_value((x, y), (x, y + 1)) +
                           self.get_value((x, y + 1), (x, y + 2))))
        if x + 1 < 7 and y + 1 < 5:
            n0 = self.get_value((x, y), (x + 1, y)) +\
                 self.get_value((x + 1, y), (x + 1, y + 1))
            n1 = self.get_value((x, y), (x, y + 1)) +\
                 self.get_value((x, y + 1), (x + 1, y + 1))
            if n0 < n1:
                points.append(([(x + 1, y), (x + 1, y + 1)], n0))
            else:
                points.append(([(x, y + 1), (x + 1, y + 1)], n1))
        if x + 1 < 7 and y - 1 >= 0:
            n0 = self.get_value((x, y), (x + 1, y)) +\
                 self.get_value((x + 1, y), (x + 1, y - 1))
            n1 = self.get_value((x, y), (x, y - 1)) +\
                 self.get_value((x, y - 1), (x + 1, y - 1))
            if n0 < n1:
                points.append(([(x + 1, y), (x + 1, y - 1)], n0))
            else:
                points.append(([(x, y - 1), (x + 1, y - 1)], n1))
        if x - 1 >= 0 and y + 1 < 5:
            n0 = self.get_value((x, y), (x - 1, y)) +\
                 self.get_value((x - 1, y), (x - 1, y + 1))
            n1 = self.get_value((x, y), (x, y + 1)) +\
                 self.get_value((x, y + 1), (x - 1, y + 1))
            if n0 < n1:
                points.append(([(x - 1, y), (x - 1, y + 1)], n0))
            else:
                points.append(([(x, y + 1), (x - 1, y + 1)], n1))
        if x - 1 >= 0 and y - 1 >= 0:
            n0 = self.get_value((x, y), (x - 1, y)) +\
                 self.get_value((x - 1, y), (x - 1, y - 1))
            n1 = self.get_value((x, y), (x, y - 1)) +\
                 self.get_value((x, y - 1), (x - 1, y - 1))
            if n0 < n1:
                points.append(([(x - 1, y), (x - 1, y - 1)], n0))
            else:
                points.append(([(x, y - 1), (x + 1, y - 1)], n1))
        res = min(points, key=lambda p: p[1])[0]
        a, b = res[-1]
        dirs = []
        if a + 1 < 7:
            dirs.append(((a + 1, b), self.get_value((a, b), (a + 1, b))))
        if a - 1 >= 0:
            dirs.append(((a - 1, b), self.get_value((a, b), (a - 1, b))))
        if b + 1 < 5:
            dirs.append(((a, b + 1), self.get_value((a, b), (a, b + 1))))
        if b - 1 >= 0:
            dirs.append(((a, b - 1), self.get_value((a, b), (a, b - 1))))
        return res, min(dirs, key=lambda w: w[1])[0]


    # это - функция, которую, получается, нужно импортировать в код с движением.
    # принимает список рёбер с их весом, координату старта, координату финиша.
    # принимает координаты у которых отсчёт начинается с 1 (н-р не (0, 0), а (1, 1))
    # возвращает путь в виде списка координат (н-р [(1, 2), (1, 3), (1, 4)]) (отсчёт тоже с 1)


def shortest_way(edges0, start, finish):
    edges = []
    start = start[0] - 1, start[1] - 1
    finish = finish[0] - 1, finish[1] - 1
    for coord in edges0:
        a = int(coord[0][0]) - 1, int(coord[0][1]) - 1
        b = int(coord[1][0]) - 1, int(coord[1][1]) - 1
        edges.append([a, b, int(coord[2])])
    board = Board(edges, start, finish)
    board.walk(start[0], start[1])
    way = board.get_way(finish[0], finish[1], [finish])[::-1]
    w, dir_point = board.calculate_finish()
    way += w
    dir_point = dir_point[0] + 1, dir_point[1] + 1
    return [(coord[0] + 1, coord[1] + 1) for coord in way], dir_point
