import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Custo do início até o nó atual
        self.h = 0  # Heurística: estimativa do custo do nó até o objetivo
        self.f = 0  # f = g + h

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def a_star(matriz, start, end):
    start_node = Node(start)
    end_node = Node(end)

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.position)

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (len(matriz) - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (len(matriz[0]) - 1) or 
                node_position[1] < 0):
                continue

            if matriz[node_position[0]][node_position[1]] in ('#', 'V', 'R'):
                continue

            new_node = Node(node_position, current_node)

            if new_node.position in closed_set:
                continue

            new_node.g = current_node.g + 1
            new_node.h = abs(new_node.position[0] - end_node.position[0]) + abs(new_node.position[1] - end_node.position[1])
            new_node.f = new_node.g + new_node.h

            if add_to_open(open_list, new_node):
                heapq.heappush(open_list, new_node)

    return None

def add_to_open(open_list, neighbor):
    for node in open_list:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

#Abrir o Ficheiro e ler todas as linhas
with open('A_Star_Algoritm/MatrizRandom_A_Star.txt', 'r') as f:
    matrizProcura = [linha.strip().split() for linha in f]
    
rows = len(matrizProcura)
cols = len(matrizProcura[0])
robot_point = 0
product_point = 0
output_point = 0

for i in range(rows):
    for j in range(cols):
        if matrizProcura[i][j] == 'R':
            robot_point = (i, j)  # Alterado de lista para tupla
        if matrizProcura[i][j] == 'P':
            product_point = (i, j)  # Alterado de lista para tupla
        if matrizProcura[i][j] == 'O':
            output_point = (i, j) 


print("\Procura do caminho um caminho ROBOT TO PRODUCT:")

caminho = a_star(matrizProcura, robot_point, product_point)

if len(caminho) > 0:
    print("Caminho encontrado:")
    for row, col in caminho:
        if matrizProcura[row][col] != 'P' or matrizProcura[row][col] != 'O':   
            matrizProcura[row][col] = 'R'
    for row in matrizProcura:
        print(' '.join(row))
    with open("A_Star_Algoritm/Output/MatrizRandom_BFS_1R_1P_1O_OUTPUT_ROBOT_VERSION.txt", "w") as file:
        for row in matrizProcura:
            file.write(' '.join(row) + '\n')
else:
    print("Caminho não encontrado.")
    

print("\Procura do caminho um caminho PRODUCT TO OUPUT:")

caminho = a_star(matrizProcura, product_point, output_point)

if len(caminho) > 0:
    print("Caminho encontrado:")
    for row, col in caminho:
        if matrizProcura[row][col] != 'P' or matrizProcura[row][col] != 'R':   
            matrizProcura[row][col] = 'O'
    for row in matrizProcura:
        print(' '.join(row))
    with open("A_Star_Algoritm/Output/MatrizRandom_BFS_1R_1P_1O_OUTPUT_EXIT_VERSION.txt", "w") as file:
        for row in matrizProcura:
            file.write(' '.join(row) + '\n')
else:
    print("Caminho não encontrado.")
