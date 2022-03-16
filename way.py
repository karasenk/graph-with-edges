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

    def mark(self, coord, n, coord0):
        x, y = coord
        weight = self.get_value(coord, coord0)
        if self.board[x][y] > n + weight:
            self.board[x][y] = n + weight
            self.graph[x][y] = coord0

    def walk(self, x, y, n):
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
    board.walk(x, y, 0)
    x1, y1 = board.finish
    way = board.get_way(x1, y1, [(x1, y1)])
    return [(coord[0] + 1, coord[1] + 1) for coord in way][::-1]
