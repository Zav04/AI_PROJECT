import heapq
import time
import pygame
import math

##########################PYGAMES FUNCTIONS#######################################
# Definindo cores
COLOR_Branco = (255, 255, 255)# Preto
COLOR_Preto = (0, 0, 0)      # Preto
COLOR_PATH = (0, 255, 0)    # Verde
COLOR_VISITED = (255, 0, 0) # Vermelho
COLOR_START = (0, 255, 255)   # Azul
COLOR_END = (252, 51, 255)  # ROSA

# Inicializa o Pygame
pygame.init()

# Define o tamanho da tela com uma resolução menor
width, height = 800, 800 
screen = pygame.display.set_mode((width, height))

# Fonte para o texto do botão
fonte = pygame.font.Font(None, 36)

def desenha_InfoBox(Screen, texto, posicao, tamanho):
    # Define a cor do texto e do fundo
    cor_texto = COLOR_Branco  
    cor_fundo = COLOR_Preto 

    # Desenha a caixa de texto
    pygame.draw.rect(Screen, cor_fundo, (*posicao, *tamanho))

    # Divide o texto em linhas
    linhas = texto.split('\n')
    linha_altura = fonte.get_height()

    # Renderiza cada linha do texto dentro da caixa
    for i, linha in enumerate(linhas):
        texto_renderizado = fonte.render(linha, True, cor_texto)
        # Ajusta a posição do texto para cada linha
        Screen.blit(texto_renderizado, (posicao[0] + 10, posicao[1] + 10 + i * linha_altura))



#Printar o mapa na janela do pygames 
def draw_matriz_init(screen, matriz, cell_size, start=None, end=None, path=None, visited=None):
    # Desenha os retângulos
    for y, row in enumerate(matriz):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if (y, x) == start:
                pygame.draw.rect(screen, COLOR_START, rect)
            elif (y, x) == end:
                pygame.draw.rect(screen, COLOR_END, rect)
            elif cell == '#':
                pygame.draw.rect(screen, COLOR_Preto, rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect)

    for y in range(len(matriz) + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, y * cell_size), (width, y * cell_size))

    # Linhas verticais
    for x in range(len(matriz[0]) + 1):
        pygame.draw.line(screen, (0, 0, 0), (x * cell_size, 0), (x * cell_size, height))
    pygame.display.flip()
    
    
    
def draw_matriz_Path(screen, matriz, cell_size, start=None, end=None, path=None, visited=None):
    # Desenha os retângulos
    for y, row in enumerate(matriz):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if visited and (y, x) in visited:
                pygame.draw.rect(screen, COLOR_VISITED, rect)
            elif path and (y, x) in path:
                pygame.draw.rect(screen, COLOR_PATH, rect)
    # Linhas Horizontais            
    for y in range(len(matriz) + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, y * cell_size), (width, y * cell_size))

    # Linhas verticais
    for x in range(len(matriz[0]) + 1):
        pygame.draw.line(screen, (0, 0, 0), (x * cell_size, 0), (x * cell_size, height))
    pygame.display.flip()


# Fonte para o texto do botão
fonte = pygame.font.Font(None, 36)

# Função para desenhar o botão
def desenha_botao(screen, texto, posicao, tamanho):
    
    # Desenha a borda (um retângulo maior atrás do botão)
    rect_borda = pygame.Rect(posicao[0] - 5, posicao[1] - 5, tamanho[0] + 2*5, tamanho[1] + 2*5)
    pygame.draw.rect(screen, COLOR_Preto, rect_borda)

    # Desenha o botão
    rect_botao = pygame.Rect(posicao[0], posicao[1], tamanho[0], tamanho[1])
    pygame.draw.rect(screen, COLOR_Preto, rect_botao)

    # Adiciona o texto ao botão
    texto_renderizado = fonte.render(texto, True, COLOR_Branco)
    text_rect = texto_renderizado.get_rect(center=rect_botao.center)
    screen.blit(texto_renderizado, text_rect)
##########################PYGAMES FUNCTIONS#######################################



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
    start_node = Node(start)  # Inicializa o nó de início
    end_node = Node(end)  # Inicializa o nó de destino
    
    open_list = []  # Lista dos nós a serem avaliados
    closed_set = set()  # Conjunto dos nós já avaliados

    heapq.heappush(open_list, start_node)  # Adiciona o nó inicial ao vector
    # Enquanto houver nós na lista aberta
    while open_list:
        
        #pygame.time.delay(500)
        draw_matriz_Path(screen, matriz, cell_size, start=robot_point, end=product_point, visited=closed_set)
        pygame.display.flip()
        
        current_node = heapq.heappop(open_list) 
        closed_set.add(current_node.position)
        # Se este nó é o destino, reconstrói o caminho
        if current_node == end_node:
            path = []
            cost=current_node.g 
            while current_node is not None:  
                path.append((current_node.position, current_node.direction))
                current_node = current_node.parent   
            return path[::-1],cost  # Retorna o caminho invertido

        # Marca o nó atual como visitado
        closed_set.add(current_node.position)

        # Gera os possíveis movimentos        
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

            # Calcula o valor de g para o novo nó. O valor g é o custo do caminho desde o nó de partida até o nó atual.
            # Este custo é a soma do valor g do nó atual (current_node.g) com o custo para se mover do nó atual para o novo nó (seu vizinho).
            new_node.g=current_node.g + compute_cost(current_node.direction, new_position)
            # Calcula o valor heurístico h para o novo nó. O valor h é uma estimativa do custo do nó atual até o nó de destino.
            # Neste caso, a heurística usada é a distância de Manhattan, que é a soma das diferenças absolutas das coordenadas x e y entre o nó atual e o nó de destino.
            new_node.h = abs(new_node.position[0] - end_node.position[0]) + abs(new_node.position[1] - end_node.position[1])
            # Calcula o valor f do novo nó. O valor f é a soma dos valores g e h.
            # f serve como uma estimativa do custo total do caminho mais curto passando por este nó. 
            # Nodes com menores valores de f são priorizados na busca.
            new_node.f = new_node.g + new_node.h 
            
            draw_matriz_Path(screen, matriz, cell_size, visited=closed_set)
            pygame.display.flip()
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

# Carrega a matriz do arquivo
with open('Matriz_Random/MatrizRandom.txt', 'r') as f:
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


# Ajusta o tamanho de cada célula
cell_size = min(width // cols, height // rows)

draw_matriz_init(screen,matrizProcura,cell_size, start=robot_point,end=product_point)
#Start Timmer
start_time = time.time()
print("Procura do caminho um caminho ROBOT TO PRODUCT:")

# Procura o caminho do robô até o produto
caminho = a_star(matrizProcura, robot_point, product_point)

# Se um caminho foi encontrado
if(caminho is not None):
    if len(caminho[0]) > 0:
        print("\033[92mCaminho encontrado:\033[0m")
        print("Custo:",caminho[1])
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
execution_time = end_time - start_time
print("Tempo de Procura: {:.15f} segundos".format(execution_time))

if(caminho is not None):
    path_positions = set((pos for pos, dir in caminho[0]))
    draw_matriz_Path(screen, matrizProcura, cell_size, start=robot_point, end=product_point, path=path_positions)
    pygame.display.flip()

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos
            rodando = False
    # Desenha o botão
    desenha_botao(screen, "Clique", (width//2, height//2), (100, 50))
    pygame.display.flip()


draw_matriz_init(screen,matrizProcura,cell_size, start=product_point,end=output_point)
start_time = time.time()
print("Procura do caminho um caminho PRODUCT TO OUPUT:")
caminho = a_star(matrizProcura, product_point, output_point)

if(caminho is not None):
    if len(caminho[0]) > 0:
        print("\033[92mCaminho encontrado:\033[0m")
        print("Custo:",caminho[1])
        # for (row, col), direcao in caminho:
        #     if matrizProcura[row][col] != 'P' and matrizProcura[row][col] != 'O' and matrizProcura[row][col] != 'R':
        #     #Se for a posição inical não existe direção por isso tem de se passar para o proximo
        #         if(direcao is None):
        #             continue
        #         matrizProcura[row][col] = direction_to_write(direcao)
        # # for row in matrizProcura:
        # #     print(' '.join(row))
        # with open("A_Star_Algoritm/Output/MatrizRandom_A_STAR_OUTPUT_EXIT_VERSION.txt", "w") as file:
        #     for row in matrizProcura:
        #         file.write(' '.join(row) + '\n')
else:
    print("\033[91mCaminho não encontrado\033[0m")

#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura: {:.15f} segundos".format(execution_time))

if(caminho is not None):
    path_positions = set((pos for pos, dir in caminho[0]))  # use um conjunto para otimizar a busca
    draw_matriz_Path(screen, matrizProcura, cell_size, start=robot_point, end=product_point, path=path_positions)
    pygame.display.flip()



# Manter a janela aberta após o caminho ser encontrado
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()