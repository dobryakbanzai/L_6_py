from collections import defaultdict


def findInCL(list, key):
    for x in list:
        if x[0] == key:
            return x[1]


def getByLTPH(LTHP, point):
    for x in LTHP:
        if x[0] == point:
            return x[1]
    return critPath[1]


def DFS(G, v, seen=None, path=None):
    if seen is None:
        seen = []
    if path is None:
        path = [v]

    seen.append(v)

    paths = []
    for t in G[v]:
        if t[0] not in seen:
            t_path = path + [t]
            paths.append(tuple(t_path))
            paths.extend(DFS(G, t[0], seen[:], t_path))
    return paths


def getMinPathToPoint(G, point):
    paths = DFS(G, '1')

    maxPathLen = 0
    maxPathb = ()
    maxPath = []
    for path in paths:
        if path[len(path) - 1][0] == point:
            pathLen = 0
            for i in range(1, len(path)):
                pathLen += path[i][1]
            if pathLen > maxPathLen:
                maxPathLen = pathLen
                maxPathb = path

    for point in maxPathb:
        if point == '1':
            maxPath.append(point)
        else:
            maxPath.append(point[0])

    return maxPath, maxPathLen


def getCritPath(G):
    paths = DFS(G, '1')

    maxPathLen = 0
    maxPathb = ()
    maxPath = []
    for path in paths:
        if path[len(path) - 1][0] == '11':
            pathLen = 0
            for i in range(1, len(path)):
                pathLen += path[i][1]
            if pathLen > maxPathLen:
                maxPathLen = pathLen
                maxPathb = path

    for point in maxPathb:
        if point == '1':
            maxPath.append(point)
        else:
            maxPath.append(point[0])

    return maxPath, maxPathLen


def getMaxPath(paths):
    m = 0
    for x in paths:
        if not (x[0] in critPath[0]) or (x[0] == '11'):
            if x[1] > m:
                m = x[1]

    return m
    # return max(x for x in [y[1] for y in paths])


def getNotCritPoints(gKey, critPath):
    return [str(x) for x in sorted(list(set([int(x) for x in gKey]) - set([int(x) for x in critPath])))]


# Описываются рёбра
edges = [
    # начальная точка [конечная точка, длина пути]
    # 1
    ['1', ['2', 14]],
    ['1', ['3', 26]],
    ['1', ['4', 8]],
    ['1', ['5', 23]],

    # 2
    ['2', ['6', 13]],
    ['2', ['7', 9]],

    # 3
    ['3', ['6', 10]],
    ['3', ['7', 24]],

    # 4
    ['4', ['6', 23]],
    ['4', ['7', 5]],

    # 5
    ['5', ['6', 7]],
    ['5', ['7', 7]],

    # 6
    ['6', ['8', 24]],
    ['6', ['9', 12]],
    ['6', ['10', 8]],

    # 7
    ['7', ['8', 9]],
    ['7', ['9', 10]],
    ['7', ['10', 23]],

    # 8
    ['8', ['11', 22]],

    # 9
    ['9', ['11', 11]],

    # 10
    ['10', ['11', 10]]

]

G = defaultdict(list)
for (s, t) in edges:
    G[s].append(t)

gKey = G.keys()

critPath = getCritPath(G)

nCritPoints = getNotCritPoints(gKey, critPath[0])

print(f"Критический путь: {critPath[0]}, с длиной {critPath[1]} \n ")

nCritPoints = list(reversed(nCritPoints))

maxPastPath = critPath[1]
endPoint = '11'

print(f"Не критические события: {nCritPoints} \n")

lthp = []
bufMax = 0

print("Наиболее поздние сроки наступления событий:")

for x in nCritPoints:
    if G[x][0][0] == endPoint:
        buf = maxPastPath - getMaxPath(G[x])
        if buf > bufMax:
            bufMax = buf
        print(f"{x}$ = {maxPastPath} - {getMaxPath(G[x])} = {buf}")
        lthp.append((x, buf))
    else:
        endPoint = G[x][0][0]
        maxPastPath = bufMax

        bufMax = 0

        buf = maxPastPath - getMaxPath(G[x])
        if buf > bufMax:
            bufMax = buf
        print(f"{x}$ = {maxPastPath} - {getMaxPath(G[x])} = {buf}")
        lthp.append((x, buf))

freeR = []
print("\nРассчет свободных резервов")
for x in gKey:
    for y in G[x]:
        if not x in critPath[0]:
            a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
            print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
            freeR.append((f"{x}-{y[0]}$", a))
        else:
            if not y[0] in critPath[0]:
                a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                freeR.append((f"{x}-{y[0]}$", a))

fullR = []
print("\nРассчет полного резерва времени:")
for x in gKey:
    for y in G[x]:
        if not x in critPath[0]:
            if y[0] in critPath[0]:
                a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR.append((f"{x}-{y[0]}$", a))
            else:
                a = getByLTPH(lthp, y[0]) - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getByLTPH(lthp, y[0])}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR.append((f"{x}-{y[0]}$", a))
        else:
            if not y[0] in critPath[0]:
                a = getByLTPH(lthp, y[0]) - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getByLTPH(lthp, y[0])}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR.append((f"{x}-{y[0]}$", a))

print('-' * 100)

edges = [
    # начальная точка [конечная точка, длина пути]
    # 1
    ['1', ['2', 14]],
    ['1', ['3', 26]],
    ['1', ['4', 8]],
    ['1', ['5', 23]],

    # 2
    ['2', ['6', 13]],
    ['2', ['7', 9]],

    # 3
    ['3', ['6', 10]],
    ['3', ['7', 24]],

    # 4
    ['4', ['6', 23]],
    ['4', ['7', 5]],

    # 5
    ['5', ['6', 7]],
    ['5', ['7', 7]],

    # 6
    ['6', ['8', 24]],
    ['6', ['9', 12]],
    ['6', ['10', 13]],

    # 7
    ['7', ['8', 9]],
    ['7', ['9', 10]],
    ['7', ['10', 23]],

    # 8
    ['8', ['11', 22]],

    # 9
    ['9', ['11', 11]],

    # 10
    ['10', ['11', 10]]

]

G = defaultdict(list)
for (s, t) in edges:
    G[s].append(t)

gKey = G.keys()

critPath = getCritPath(G)

nCritPoints = getNotCritPoints(gKey, critPath[0])

print(f"Критический путь: {critPath[0]}, с длиной {critPath[1]} \n ")

nCritPoints = list(reversed(nCritPoints))

maxPastPath = critPath[1]
endPoint = '11'

print(f"Не критические события: {nCritPoints} \n")

lthp = []
bufMax = 0

print("Наиболее поздние сроки наступления событий:")

for x in nCritPoints:
    if G[x][0][0] == endPoint:
        buf = maxPastPath - getMaxPath(G[x])
        if buf > bufMax:
            bufMax = buf
        print(f"{x}$ = {maxPastPath} - {getMaxPath(G[x])} = {buf}")
        lthp.append((x, buf))
    else:
        endPoint = G[x][0][0]
        maxPastPath = bufMax

        bufMax = 0

        buf = maxPastPath - getMaxPath(G[x])
        if buf > bufMax:
            bufMax = buf
        print(f"{x}$ = {maxPastPath} - {getMaxPath(G[x])} = {buf}")
        lthp.append((x, buf))

freeR1 = []
print("\nРассчет свободных резервов")
for x in gKey:
    for y in G[x]:
        if not x in critPath[0]:
            a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
            print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
            freeR1.append((f"{x}-{y[0]}$", a))
        else:
            if not y[0] in critPath[0]:
                a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                freeR1.append((f"{x}-{y[0]}$", a))

fullR1 = []
print("\nРассчет полного резерва времени:")
for x in gKey:
    for y in G[x]:
        if not x in critPath[0]:
            if y[0] in critPath[0]:
                a = getMinPathToPoint(G, y[0])[1] - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getMinPathToPoint(G, y[0])[1]}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR1.append((f"{x}-{y[0]}$", a))
            else:
                a = getByLTPH(lthp, y[0]) - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getByLTPH(lthp, y[0])}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR1.append((f"{x}-{y[0]}$", a))
        else:
            if not y[0] in critPath[0]:
                a = getByLTPH(lthp, y[0]) - getMinPathToPoint(G, x)[1] - y[1]
                print(f"{x}-{y[0]}$ = {getByLTPH(lthp, y[0])}-{getMinPathToPoint(G, x)[1]}-{y[1]}={a}")
                fullR1.append((f"{x}-{y[0]}$", a))

print("\nСравнение свободных резервов")

for i in freeR:
    print(i[0], i[1], findInCL(freeR1, i[0]))

print("\n", set(freeR) - set(freeR1))

print("\nСравнение полных резервов")

for i in fullR:
    print(i[0], i[1], findInCL(fullR1, i[0]))

print("\n", set(fullR) - set(fullR1))