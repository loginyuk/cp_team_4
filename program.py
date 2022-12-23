'''Finding the shortest path between two points surface'''
import math

def read_file(path):
    """
    This function reads the file and returns a list of lists
    """
    array = []
    with open(path, 'r', encoding='utf8') as file:
        file.readline()
        file.readline()
        file.readline()
        for row in file:
            row = row.split()
            array.append(list(map(float, row)))
    return array

def make_a_squar(array):
    """
    This function makes a square from a list of lists
    """
    if len(array) > len(array[0]):
        diff = len(array) - len(array[0])
        arratlen = len(array)
        for i in range(arratlen):
            for _ in range(diff):
                array[i].append(math.inf)
    elif len(array) < len(array[0]):
        diff = len(array[0]) - len(array)
        elem = [99999999 for _ in range(len(array[0]))]
        for _ in range(diff):
            array.append(elem)
    return array

def distance(array, step):
    """
    s = sqrt((h1-h2)^2 + step^2)
    M[i][j] - M[i][j+1]
    M[i][j] - M[i+1][j]

    input ->
    M ---
    [[4, 7, 2],
    [1, 2, 3],
    [4, 2, 6]]

    step --- integer

    outut ->
    [[(0,0), (0,1), s1],
    [(0,1), (0,2), s2],
    [(1,0), (1,1) s3],
    [(1,1), (1,2), s4 ],
    [(2,0), (2,1), s5 ],
    [(2,1), (2, 2), s6],
    [(0,0), (1,0), s7],
    [(1,0), (2,0), s8],
    [(0,1), (1,1), s9],
    [(1,1), (2,1), s10],
    [(0,2), (1,2), s11],
    [(1,2), (2, 2), s12]]
    """
    lst = []
    dicted = {}
    array_len = len(array)
    for i in range(array_len):
        for j in range(len(array[i])):
            if j<len(array[i]) - 1:
                step_i = round(math.sqrt((array[i][j] - array[i][j+1])**2 + step ** 2) ,2)
                lst.append([(i,j), (i,j+1), step_i])
            if i<len(array[i]) - 1:
                step_i = round(math.sqrt((array[i][j] - array[i+1][j])**2 + step ** 2), 2)
                lst.append([(i,j), (i+1,j), step_i])
    lst_len = len(lst)
    for i in range(lst_len):
        lst.append([lst[i][1], lst[i][0], lst[i][2]])
    lst_len = len(lst)
    for i in range(lst_len):
        if lst[i][0] not in dicted:
            dicted[lst[i][0]] = [lst[i][1:]]
        else:
            dicted[lst[i][0]].append(lst[i][1:])
    return dicted

def dijkstra(graph, start, goal):
    '''
    The function performs Dijkstra's algorithm to find the shortest path
    >>> dijkstra(distance(make_a_squar(read_file('myex.csv')), 5), (0,0), (39, 2))
    'The distance of path is 205.2\\nThis is your path: [(0, 0), (1, 0), (2, 0), (3, 0), \
(4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), \
(14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), \
(23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0), (31, 0), \
(32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (39, 1), (39, 2)]'
    '''

    shortest_distances = {} # словник містить відстані від початку до всіх точок
    previous = {} # словник містить попередників для всіх точок
    unseen_nodes = graph # Це список точок, які ми ще не відвідали,
                         # ми будемо видаляти з нього точки, які ми відвідаємо
    path = [] # фінальний шлях, який ми повернемо

    for node in unseen_nodes:
        shortest_distances[node] = math.inf # всі відстані починаються з бескінечності
    shortest_distances[start] = 0 # відстань до початкової точки завжди 0

    while unseen_nodes: # поки є точки, які ми ще не відвідали
        min_node = None
        min_distance = math.inf
        for node in unseen_nodes: # ітеруємося по всіх точках, які ми ще не відвідали
            s_distance = shortest_distances[node] # відстань до поточної точки
            if min_node is None or s_distance < min_distance: # якщо поточна точка ще не визначена
                                                              # або відстань до поточної точки менша
                                                              # за мінімальну відстань
                min_node = node # встановлюємо поточну точку як мінімальну
                min_distance = s_distance # встановлюємо відстань
                                          # до поточної точки як мінімальну відстань

        possible_path = graph[min_node] # список можливих шляхів від поточної точки
        min_distance = shortest_distances[min_node] # відстань до поточної точки
        for next_node, weight in possible_path:
            # якщо вага поточного шляху + відстань до поточної точки менша
            # за відстань до наступної точки, то оновлюємо відстань до наступної точки
            if weight + min_distance < shortest_distances[next_node]:
                shortest_distances[next_node] = weight + min_distance
                previous[next_node] = min_node # встановлюємо поточну точку
                                               # як попередник наступної точки

        unseen_nodes.pop(min_node) # видаляємо поточну точку зі списку точок, які ми ще не відвідали
    curent = goal
    while curent != start: # поки поточна точка не дорівнює початковій точці
        try:
            path.insert(0, curent) # вставляємо поточну точку в початок шляху
            curent = previous[curent] # встановлюємо поточну точку як попередник поточної точки
        except KeyError:
            return 'There is no path between the start and the goal'
    path.insert(0,start) # вставляємо початкову точку в початок шляху

    try:
        if shortest_distances[goal] != math.inf:
            shortest_distances[goal] = shortest_distances[goal]
    except KeyError:
        return 'There is no path between the start and the goal'
    if shortest_distances[goal] != math.inf:
        return f'The distance of path is {round(shortest_distances[goal], 2)}\n\
This is your path: {path}'

print(dijkstra(distance(make_a_squar(read_file('myex.csv')), 5), (0,0), (39, 2)))

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
