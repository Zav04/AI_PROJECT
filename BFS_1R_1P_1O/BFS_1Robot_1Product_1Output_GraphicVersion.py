import time
import pygame

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
def desenha_botao(tela, texto, posicao, tamanho):
    
    # Desenha a borda (um retângulo maior atrás do botão)
    rect_borda = pygame.Rect(posicao[0] - 5, posicao[1] - 5, tamanho[0] + 2*5, tamanho[1] + 2*5)
    pygame.draw.rect(tela, COLOR_Preto, rect_borda)

    # Desenha o botão
    rect_botao = pygame.Rect(posicao[0], posicao[1], tamanho[0], tamanho[1])
    pygame.draw.rect(tela, COLOR_Preto, rect_botao)

    # Adiciona o texto ao botão
    texto_renderizado = fonte.render(texto, True, COLOR_Branco)
    text_rect = texto_renderizado.get_rect(center=rect_botao.center)
    tela.blit(texto_renderizado, text_rect)
##########################PYGAMES FUNCTIONS#######################################


##BFS não considera o custo do caminho por isso tem de se otimizar para outro algoritmo
class BFS:
    # Construtor da classe BFS que inicializa a matriz, dimensões, e as matriz de pontos visitados
    def __init__(self, matriz):
        self.matriz = matriz  # A matriz de entrada representando o labirinto
        self.rows = len(matriz)  # O número de linhas no labirinto
        self.cols = len(matriz[0]) if self.rows > 0 else 0  # O número de colunas no labirinto
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para rastrear se cada posição que foi visitada
        self.prev = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para armazenar a ponto anterior no caminho mais curto

    def clean(self):
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para rastrear se cada posição que foi visitada
        self.prev = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para armazenar a ponto anterior no caminho mais curto


    # Método que executa a busca em largura (BFS) a partir do ponto inical
    def solve(self, start_row, start_col,searchType):
        q = [(start_row, start_col)]  # Um vector que contém os pontos a serem visitados, começando pelo ponto de início
        self.visited[start_row][start_col] = True 
        visitado = set()
        visitado.add((start_row, start_col))# Marca a ponto de início como visitada
        
        # Continua até que todas os pontos possíveis tenham sido visitadas
        while q:
            row, col = q.pop(0) # Remove e retorna o primeiro elemento da lista
            #Desenha caminhos visitados
            draw_matriz_Path(screen, matrizProcura, cell_size, start=robot_point, end=product_point, visited= visitado)
            pygame.display.flip()

            # Se o ponto atual é o destino, retorna a matriz de caminhos anteriores
            if self.matriz[row][col] == searchType:
                return self.prev
            # Verifica todas as quatro direções a partir da ponto atual
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                #(-1, 0): Este é um movimento para cima.
                #(1, 0): Este é um movimento para baixo.
                #(0, -1): Este é um movimento para a esquerda.
                #(0, 1): Este é um movimento para a direita.
                next_row, next_col = row + dx, col + dy  # Calcula o proximo ponto nas direções

                # Se o proximo ponto é válida (dentro dos limites e não um obstáculo) e não foi visitada, adiciona à fila
                if (0 <= next_row < self.rows and 0 <= next_col < self.cols and 
                    not self.visited[next_row][next_col] and 
                    self.matriz[next_row][next_col] != '#'):
                    
                    q.append((next_row, next_col))  # Adiciona o proximo ponto à fila
                    self.visited[next_row][next_col] = True  # Marca o proximo ponto como visitada
                    self.prev[next_row][next_col] = (row, col) 
                    visitado.add((next_row, next_col)) # Armazena a ponto atual como a ponto anterior para o proximo ponto
                    #Desenha caminhos visitados
                    draw_matriz_Path(screen, matrizProcura, cell_size, start=robot_point, end=product_point, visited= visitado)
                    pygame.display.flip()

        return None  # Se não encontrar um caminho, retorna None

    # Método para reconstruir o caminho do destino até o início
    def reconstruct_path(self, start_row, start_col, end_row, end_col):
        path = []  # Lista para armazenar o caminho reconstruído
        row, col = end_row, end_col  # Começa pelo fim
        # Continua até que o início seja alcançado
        while (row, col) != (start_row, start_col):
            path.append((row, col))  # Adiciona o ponto atual ao caminho
            row, col = self.prev[row][col]  # Move para a ponto anterior no caminho
        path.append((start_row, start_col))  # Adiciona a ponto de início ao caminho
        return path[::-1]  # Retorna o caminho invertido (do início para o fim)

    # Método para iniciar a busca em largura e reconstruir o caminho, se encontrado
    def search(self, start_row, start_col, end_row, end_col,searchType):
        prev = self.solve(start_row, start_col,searchType)  # Realiza a busca em largura
        if prev is None:
            return []
        # Se um caminho for encontrado, reconstrói e retorna o caminho
        return self.reconstruct_path(start_row, start_col, end_row, end_col)

#Abrir o Ficheiro e ler todas as linhas
with open('Matriz_Random/MatrizRandom.txt', 'r') as f:
    matrizProcura = [linha.strip().split() for linha in f]  # Lê cada linha do ficheiro, remove espaços em branco


# Cria um filho da classe BFS
bfs_search= BFS(matrizProcura)  # Inicializa a classe BFS com a matriz do labirinto

# Obter o número de linhas e colunas do labirinto
rows = len(matrizProcura)
cols = len(matrizProcura[0])

# Inicializar variáveis para as coordenadas do robô, produto e saída
robot_row,robot_col,product_row,product_col,output_row,output_col = 0,0,0,0,0,0

# Procurar as coordenadas do robô, produto e saída no labirinto
for i in range(rows):
    for j in range(cols):
        if matrizProcura[i][j] == 'R':
            robot_row = i
            robot_col = j
        if matrizProcura[i][j] == 'P':
            product_row = i
            product_col = j
        if matrizProcura[i][j] == 'O':
            output_row = i
            output_col = j

#Passar de cordenadas para pontos
robot_point=robot_row,robot_col  
product_point=product_row,product_col 
output_point=output_row,output_col

# Ajusta o tamanho de cada célula
cell_size = min(width // cols, height // rows)

#Printar o mapa na janela do pygames
draw_matriz_init(screen,matrizProcura,cell_size, start=robot_point,end=product_point)

#Start Timmer
start_time = time.time()

print("Procura do caminho um caminho ROBOT TO PRODUCT:")
Robot2Product_path = bfs_search.search(robot_row, robot_col, product_row, product_col,'P')  # Procura o caminho do robô até o produto
if len(Robot2Product_path) > 0:  # Se um caminho foi encontrado
    print("\033[92mCaminho encontrado:\033[0m")
    # for row, col in Robot2Product_path:  # Para cada ponto no caminho
    #     if matrizProcura[row][col] != 'P' or matrizProcura[row][col] != 'O':   
    #         matrizProcura[row][col] = 'R'  # Marca o caminho com 'R'
    # with open("BFS_1R_1P_1O/Output/MatrizRandom_BFS_1R_1P_1O_OUTPUT_ROBOT_VERSION.txt", "w") as file:
    #     for row in matrizProcura:
    #         file.write(' '.join(row) + '\n')  
else:
    print("\033[91mCaminho não encontrado\033[0m")  # Se não houver caminho
#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura: {:.15f} segundos".format(execution_time))

#Mostrar na janela o Path encontrado
draw_matriz_Path(screen, matrizProcura, cell_size, start=robot_point, end=product_point, path=Robot2Product_path)
pygame.display.flip()

# Atualiza a matriz do objeto para a próxima busca
#bfs_search.matriz= matrizProcura
bfs_search.clean()

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








#Printar o mapa na janela do pygames
draw_matriz_init(screen,matrizProcura,cell_size, start=product_point,end=output_point)
#Start Timmer
start_time = time.time()

# Procura do caminho do produto até a saída
print("Procura do caminho um caminho PRODUCT TO OUTPUT :")
Product2Output_path = bfs_search.search(product_row, product_col, output_row, output_col,'O')  # Procura o caminho do produto até a saída
if len(Product2Output_path) > 0:  # Se um caminho foi encontrado
    print("\033[92mCaminho encontrado:\033[0m")
    for row, col in Product2Output_path:  # Para cada ponto no caminho
        if matrizProcura[row][col] != 'P' or matrizProcura[row][col] != 'R':  
            matrizProcura[row][col] = 'O'  # Marca o caminho com 'O'
    # for row in matrizProcura:
    #     print(' '.join(row))  # Print do labirinto com o caminho marcado
    # Escreve o labirinto com o caminho do Output
    with open("BFS_1R_1P_1O/Output/MatrizRandom_BFS_1R_1P_1O_OUTPUT_EXIT_VERSION.txt", "w") as file:
        for row in matrizProcura:
            file.write(' '.join(row) + '\n') 
else:
    print("\033[91mCaminho não encontrado\033[0m")  # Se não houver caminho

#Mostrar na janela o Path encontrado
draw_matriz_Path(screen, matrizProcura, cell_size, start=product_point, end=output_point, path=Product2Output_path)
pygame.display.flip()

#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura: {:.15f} segundos".format(execution_time))


# Manter a janela aberta após o caminho ser encontrado
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
