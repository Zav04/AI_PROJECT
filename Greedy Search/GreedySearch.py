import heapq
import time
import pygame
import math
import glob
import time
import pandas as pd
from openpyxl import Workbook
import glob
import os

# Define uma classe para representar os nós
class Node:
    # Construtor da classe
    def __init__(self, position, parent=None, direction=None):
        self.position = position  # Define a posição atual do nó
        self.parent = parent  # Define o nó pai (de onde veio)
        self.direction = direction  # Define a direção de movimento
        self.g = 0  # Custo do caminho desde o início até o nó
        self.h = 0  # Custo estimado do nó até o objetivo (heurística)
        self.f = 0  # Soma de g e h

    # Sobrescreve o operador de igualdade para comparar nós pelo 'position'
    def __eq__(self, other):
        return self.position == other.position

    # Sobrescreve o operador de menor para comparação baseada em 'f'
    def __lt__(self, other):
        return self.f < other.f

# Função para calcular o custo do movimento baseado na direção
def compute_cost(last_direction, next_direction):
    cost = 1  # Custo base do movimento
    # Se mudar de direção, adiciona um custo adicional
    if last_direction != next_direction:
        cost += 1
    return cost

# Função principal do algoritmo
def a_star(matriz, start, end):
    i_Manhattan=0
    start_node = Node(start)  # Inicializa o nó de início
    end_node = Node(end)  # Inicializa o nó de destino
    
    i_Manhattan=end_node.position[0]-start_node.position[0]+end_node.position[1]-start_node.position[1]
    open_list = []  # Lista dos nós a serem avaliados
    closed_set = set()  # Conjunto dos nós já avaliados

    heapq.heappush(open_list, start_node)  # Adiciona o nó inicial ao vector
    # Enquanto houver nós na lista aberta
    while open_list:
        current_node = heapq.heappop(open_list) 
        closed_set.add(current_node.position)
        # Se este nó é o destino, reconstrói o caminho
        if current_node == end_node:
            path = []
            cost=0
            while current_node is not None:  
                path.append((current_node.position, current_node.direction))
                if current_node.parent and current_node.direction:
                    cost = cost + compute_cost(current_node.parent.direction, current_node.direction)
                current_node = current_node.parent   
            return path[::-1],cost
        
# Retorna o caminho invertido
        # Marca o nó atual como visitado
        closed_set.add(current_node.position)  # Retorna o caminho invertido

        # Marca o nó atual como visitado
        closed_set.add(current_node.position)

        # Gera os possíveis movimentos
        # for new_position in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        
        for new_position in [(0, -1), (0, 1),(-1, 0), (1, 0) ]:
            #(-1, 0): Este é um movimento para cima.
            #(1, 0): Este é um movimento para baixo.
            #(0, -1): Este é um movimento para a esquerda.
            #(0, 1): Este é um movimento para a direita.
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Verifica se a posição está dentro dos limites da matriz
            if (node_position[0] > (len(matriz) - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (len(matriz[0]) - 1) or 
                node_position[1] < 0):
                continue

            # Se a posição é um obstáculo passa para outra iteração de movimento
            if matriz[node_position[0]][node_position[1]] in ('#'):
                continue
            
            # Cria um novo nó e define seu 'g', 'h', e 'f'
            new_node = Node(node_position, current_node, direction=new_position)
            # Se o nó já foi avaliado então passa para outra iteração de movimento
            if new_node.position in closed_set:
                continue

            #Calculo do custo será sempre zero apenas será calculado o valor heurístico
            new_node.g = 0
            #new_node.g=current_node.g + compute_cost(current_node.direction, new_position)
            # Calcula o valor heurístico h para o novo nó. O valor h é uma estimativa do custo do nó atual até o nó de destino.
            # Neste caso, a heurística usada é a distância de Manhattan, que é a soma das diferenças absolutas das coordenadas x e y entre o nó atual e o nó de destino.
            new_node.h = abs(new_node.position[0] - end_node.position[0]) + abs(new_node.position[1] - end_node.position[1])
            # Calcula o valor f do novo nó. O valor f é a soma dos valores g e h.
            # f serve como uma estimativa do custo total do caminho mais curto passando por este nó. 
            # Nodes com menores valores de f são priorizados na busca.
            new_node.f = new_node.g + new_node.h 
            
            # Se o nó é uma nova adição ao vector
            if add_to_open(open_list, new_node):
                heapq.heappush(open_list, new_node)

    return None  # Retorna None se não encontrar um caminho

#OpenList é um conjunto de nós que foram descobertos, mas ainda não explorados.
def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node:
            if neighbor.f < node.f:
                node.g = neighbor.g
                node.h = neighbor.h
                node.f = neighbor.f
                node.parent = neighbor.parent
                node.direction = neighbor.direction
            return False
    return True


base_path = './Matriz_Random'

# Constrói o padrão de busca para encontrar todos os arquivos .txt em todos os subdiretórios
search_pattern = os.path.join(base_path, '**', '*.txt')

# Usa glob com a opção recursive=True para buscar em todos os subdiretórios
file_paths = glob.glob(search_pattern, recursive=True)
# Lista para armazenar os resultados
results = []

for file_path in file_paths:
    with open(file_path, 'r') as f:
        matrizProcura = [linha.strip().split() for linha in f] 

    # Obter o número de linhas e colunas do labirinto    
    rows = len(matrizProcura)
    cols = len(matrizProcura[0])

    # Inicializar variáveis para as coordenadas do robô, produto e saída
    robot_point,product_point,output_point = 0,0,0

    # Procurar as coordenadas do robô, produto e saída no labirinto
    for i in range(rows):
        for j in range(cols):
            if matrizProcura[i][j] == 'R':
                robot_point = (i, j)  
            if matrizProcura[i][j] == 'P':
                product_point = (i, j) 
            if matrizProcura[i][j] == 'O':
                output_point = (i, j) 


    print("Matriz de Procura:",file_path)
    #Start Timmer
    start_time = time.time()
    print("Procura do caminho um caminho ROBOT TO PRODUCT:")

    # Procura o caminho do robô até o produto
    caminhoRobot2Product = a_star(matrizProcura, robot_point, product_point)

    # Se um caminho foi encontrado
    if(caminhoRobot2Product is not None):
        if len(caminhoRobot2Product[0]) > 0:
            print("\033[92mCaminho encontrado:\033[0m")
            print("Custo:",caminhoRobot2Product[1])
            # for (row, col), direcao in caminho: # Para cada ponto no caminho e a direção
            #     if matrizProcura[row][col] != 'P' and matrizProcura[row][col] != 'O' and matrizProcura[row][col] != 'R':
            #         #Se for a posição inical não existe direção por isso tem de se passar para o proximo
            #         if(direcao is None):
            #             continue
            #         matrizProcura[row][col] = direction_to_write(direcao)
            # # for row in matrizProcura:
            # #     print(' '.join(row))
            # with open("A_Star_Algoritm/Output/MatrizRandom_A_STAR_ROBOT_VERSION.txt", "w") as file:
            #     for row in matrizProcura:
            #         file.write(' '.join(row) + '\n')
    else:
        print("\033[91mCaminho não encontrado\033[0m")

    #End Timmer
    end_time = time.time()
    #Saber tempo de processamento
    execution_time_rp = end_time - start_time
    print("Tempo de Procura: {:.15f} segundos".format(execution_time_rp))


    start_time = time.time()
    print("Procura do caminho um caminho PRODUCT TO OUPUT:")
    caminhoProduct2Output = a_star(matrizProcura, product_point, output_point)

    # Se um caminho foi encontrado
    if(caminhoProduct2Output is not None):
        if len(caminhoProduct2Output[0]) > 0:
            print("\033[92mCaminho encontrado:\033[0m")
            print("Custo:",caminhoProduct2Output[1])
            # for (row, col), direcao in caminho: # Para cada ponto no caminho e a direção
            #     if matrizProcura[row][col] != 'P' and matrizProcura[row][col] != 'O' and matrizProcura[row][col] != 'R':
            #         #Se for a posição inical não existe direção por isso tem de se passar para o proximo
            #         if(direcao is None):
            #             continue
            #         matrizProcura[row][col] = direction_to_write(direcao)
            # # for row in matrizProcura:
            # #     print(' '.join(row))
            # with open("A_Star_Algoritm/Output/MatrizRandom_A_STAR_ROBOT_VERSION.txt", "w") as file:
            #     for row in matrizProcura:
            #         file.write(' '.join(row) + '\n')
    else:
        print("\033[91mCaminho não encontrado\033[0m")

    #End Timmer
    end_time = time.time()
    #Saber tempo de processamento
    execution_time_po = end_time - start_time
    print("Tempo de Procura: {:.15f} segundos".format(execution_time_po))


    results.append({
            'File Path': file_path,
            'Cost Robot to Product': caminhoRobot2Product[1] if caminhoRobot2Product else None,
            'Cost Product to Output': caminhoProduct2Output[1] if caminhoProduct2Output else None,
            'Execution Time Robot to Product': execution_time_rp,
            'Execution Time Product to Output': execution_time_po
        })

# Cria um DataFrame com os resultados
df_results = pd.DataFrame(results)

# Exporta o DataFrame para um arquivo Excel
df_results.to_excel('GridySearch_Results.xlsx', index=False)