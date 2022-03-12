from way import shortest_way

alphabet = {'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ж': 7}
f = open('data.txt', 'r', encoding='utf-8')
e = eval(f.read())
f.close()
edges = []
for coord in e:
    a = alphabet[coord[0][0]], int(coord[0][1])
    b = alphabet[coord[1][0]], int(coord[1][1])
    edges.append([a, b, int(coord[2])])

print(shortest_way(edges, (1, 3), (4, 5)))
