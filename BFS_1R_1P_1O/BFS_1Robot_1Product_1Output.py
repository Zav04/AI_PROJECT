import time
##BFS não considera o custo do caminho por isso tem de se otimizar para outro algoritmo
class BFS:
    # Construtor da classe BFS que inicializa a matriz, dimensões, e as matriz de pontos visitados
    def __init__(self, matriz):
        self.matriz = matriz  # A matriz de entrada representando o labirinto
        self.rows = len(matriz)  # O número de linhas no labirinto
        self.cols = len(matriz[0]) if self.rows > 0 else 0  # O número de colunas no labirinto
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para rastrear se cada posição que foi visitada
        self.prev = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para armazenar a ponto anterior no caminho mais curto

    def clear(self):
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  
        self.prev = [[None for _ in range(self.cols)] for _ in range(self.rows)] 
        
    # Método que executa a busca em largura (BFS) a partir do ponto inical
    def solve(self, start_row, start_col):
        q = [(start_row, start_col)]  # Um vector que contém os pontos a serem visitados, começando pelo ponto de início
        self.visited[start_row][start_col] = True  # Marca a ponto de início como visitada

        # Continua até que todas os pontos possíveis tenham sido visitadas
        while len(q) > 0:
            row, col = q.pop(0)  # Remove e retorna o primeiro elemento da fila

            # Se o ponto atual é o destino, retorna a matriz de caminhos anteriores
            if self.matriz[row][col] == 'P' or self.matriz[row][col] == 'O':
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
                    self.prev[next_row][next_col] = (row, col)  # Armazena a ponto atual como a ponto anterior para o proximo ponto
        return None  # Se não encontrar um caminho, retorna None

    # Método para reconstruir o caminho do destino até o início
    def reconstruct_path(self, start_row, start_col, end_row, end_col):
        path = []  # Lista para armazenar o caminho reconstruído
        row, col = end_row, end_col  # Começa pelo fim
        # Continua até que o início seja alcançado
        while (row, col) != (start_row, start_col):
            path.append((row, col))  # Adiciona o ponto atual ao caminho
            if self.prev[row][col] is None:  # verifica se chegamos a um ponto sem predecessor
                return []
            row, col = self.prev[row][col]  # Move para a ponto anterior no caminho
        path.append((start_row, start_col))  # Adiciona a ponto de início ao caminho
        return path[::-1]  # Retorna o caminho invertido (do início para o fim)

    # Método para iniciar a busca em largura e reconstruir o caminho, se encontrado
    def search(self, start_row, start_col, end_row, end_col):
        prev = self.solve(start_row, start_col)  # Realiza a busca em largura
        if prev is None:
            return []
        # Se um caminho for encontrado, reconstrói e retorna o caminho
        return self.reconstruct_path(start_row, start_col, end_row, end_col)

#Abrir o Ficheiro e ler todas as linhas
with open('BFS_1R_1P_1O/MatrizRandom_BFS_1R_1P_1O.txt', 'r') as f:
    matrizProcura = [linha.strip().split() for linha in f]  # Lê cada linha do ficheiro, remove espaços em branco

# print("Labirinto:")  # Print do labirinto original
# for row in matrizProcura:
#     print(' '.join(row)) 

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

#Start Timmer
start_time = time.time()

print("\Procura do caminho um caminho ROBOT TO PRODUCT:")
Robot2Product_path = bfs_search.search(robot_row, robot_col, product_row, product_col)  # Procura o caminho do robô até o produto
if len(Robot2Product_path) > 0:  # Se um caminho foi encontrado
    print("Caminho encontrado:")
    for row, col in Robot2Product_path:  # Para cada ponto no caminho
        if matrizProcura[row][col] != 'P' or matrizProcura[row][col] != 'O':   
            matrizProcura[row][col] = 'R'  # Marca o caminho com 'R'
    # for row in matrizProcura:
    #     print(' '.join(row))  # Print do labirinto com o caminho marcado
    # Escreve o labirinto com o caminho do robot
    with open("BFS_1R_1P_1O/Output/MatrizRandom_BFS_1R_1P_1O_OUTPUT_ROBOT_VERSION.txt", "w") as file:
        for row in matrizProcura:
            file.write(' '.join(row) + '\n')  
else:
    print("Caminho não encontrado.")  # Se não houver caminho
#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura:",execution_time)

# Atualiza a matriz do objeto para a próxima busca
bfs_search.matriz= matrizProcura

#Limpa Vectores de previsão de caminhos visitados
BFS.clear(bfs_search)

#Start Timmer
start_time = time.time()

# Procura do caminho do produto até a saída
print("\Procura do caminho um caminho PRODUCT TO OUTPUT :")
Product2Output_path = bfs_search.search(product_row, product_col, output_row, output_col)  # Procura o caminho do produto até a saída
if len(Product2Output_path) > 0:  # Se um caminho foi encontrado
    print("Caminho encontrado:")
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
    print("Caminho não encontrado.")  # Se não houver caminho

#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura:",execution_time)
