import time
class BFS:
    # Construtor da classe BFS que inicializa a matriz, dimensões, e as matriz de pontos visitados
    def __init__(self, matriz):
        self.matriz = matriz  # A matriz de entrada representando o labirinto
        self.rows = len(matriz)  # O número de linhas no labirinto
        self.cols = len(matriz[0]) if self.rows > 0 else 0  # O número de colunas no labirinto
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para rastrear se cada posição que foi visitada
        self.prev = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Uma matriz para armazenar a ponto anterior no caminho mais curto

    # Método que executa a busca em largura (BFS) a partir do ponto inical
    def solve(self, start_row, start_col):
        q = [(start_row, start_col)]  # Um vector que contém os pontos a serem visitados, começando pelo ponto de início
        self.visited[start_row][start_col] = True  # Marca a ponto de início como visitada

        # Continua até que todas os pontos possíveis tenham sido visitadas
        while q:
            row, col = q.pop(0)  # Remove e retorna o primeiro elemento da fila

            # Se o ponto atual é o destino, retorna a matriz de caminhos anteriores
            if self.matriz[row][col] == 'P':
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




# Lê o labirinto do arquivo e armazena em uma matriz
with open('BFS_1_To_1/MatrizRandom_BFS_1_To_1.txt', 'r') as f:
    matriz = [linha.strip().split() for linha in f]  

# Cria uma instância da classe BFS
bfs_search = BFS(matriz)  

start_row, start_col, end_row, end_col = 0, 0, 0, 0  # Inicializa as variáveis de início e fim

# Procura as posições de início e fim no labirinto
for i in range(bfs_search.rows):
    for j in range(bfs_search.cols):
        if matriz[i][j] == 'R':
            start_row, start_col = i, j  # Define a posição de início
        elif matriz[i][j] == 'P':
            end_row, end_col = i, j  # Define a posição de fim

# print("Labirinto:")  # Imprime o labirinto original
# for row in matriz:
#     print(' '.join(row))

#Start Timmer
start_time = time.time()
print("\nProcura do caminho:")  # Inicia a busca pelo caminho
path = bfs_search.search(start_row, start_col, end_row, end_col)

# Se um caminho for encontrado, marca o caminho no labirinto e imprime o resultado
if path:
    print("\033[92mCaminho encontrado:\033[0m")
    for row, col in path:
        if matriz[row][col] != 'P':
            matriz[row][col] = 'R'  # Marca os pontos do caminho como 'R'
    # for row in matriz:
    #     print(' '.join(row))  # Imprime o labirinto com o caminho
    with open("BFS_1_To_1/Output/MatrizRandom_BFS_1_To_1_OUTPUT.txt", "w") as file:
        for row in matriz:
            file.write(' '.join(row) + '\n')  # Salva o labirinto com o caminho em um arquivo
else:
    print("\033[91mCaminho não encontrado\033[0m")  # Se não houver caminho

#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Procura: {:.15f} segundos".format(execution_time))
