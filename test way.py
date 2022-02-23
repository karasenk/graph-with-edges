from way import shortest_way

alphabet = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6}
f = open('data.txt', 'r', encoding='utf-8')
e = eval(f.read())
f.close()
edges = []
for coord in e:
    a = alphabet[coord[0][0]], int(coord[0][1])
    b = alphabet[coord[1][0]], int(coord[1][1])
    edges.append([a, b, int(coord[2])])

print(shortest_way(edges, (1, 3), (7, 1)))
