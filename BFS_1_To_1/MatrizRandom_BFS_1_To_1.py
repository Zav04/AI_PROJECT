import random
import time

# Função para criar a matriz com a percentagem desejada de 1s e um ponto 'P'
def create_matrix(rows, cols, percentageobstacles):
    # Cria uma matriz com 'rows' linhas e 'cols' colunas, inicialmente preenchida com '.'
    matrix = [['.' for _ in range(cols)] for _ in range(rows)]
    
    # Calcula um número aleatório de # a serem colocados na matriz, baseado nas percentagens fornecidas
    num_ones = random.randint(rows * cols * percentageobstacles // 100, rows * cols * percentageobstacles // 100)

    # Cria uma lista de todas as posições possíveis na matriz
    positions = [(i, j) for i in range(rows) for j in range(cols)]
    random.shuffle(positions)  # Mistura as posições

    # Coloca '#' nas primeiras 'num_ones' posições após misturar
    for i, j in positions[:num_ones]:
        matrix[i][j] = '#'

    # Adiciona 'R' (robô) e 'P' (produto) em posições aleatórias diferentes das que têm '#'
    robot_position = (0,0)
    product_position = random.choice(positions[num_ones:])
    # Certifica que 'R' e 'P' não são colocados na mesma posição
    while robot_position == product_position:
        product_position = random.choice(positions[num_ones:])

    matrix[robot_position[0]][robot_position[1]] = 'R'  # Coloca 'R' na posição escolhida
    matrix[product_position[0]][product_position[1]] = 'P'  # Coloca 'P' na posição escolhida

    return matrix  # Retorna a matriz criada


#Start Timmer
start_time = time.time()

# Cria a matriz com X linhas e Y colunas, com XX% de '#' nas linhas e nas colunas
matrix = create_matrix(10, 10, 30)

# # Imprime a matriz, linha por linha
# for row in matrix:
#     print(' '.join(map(str, row)))  # Print dos elementos da matriz

# Guarda a matriz
with open("BFS_1_To_1/MatrizRandom_BFS_1_To_1.txt", "w") as file:
    for row in matrix:
        file.write(' '.join(row) + '\n')  # Escreve cada linha da matriz


#End Timmer
end_time = time.time()
#Saber tempo de processamento
execution_time = end_time - start_time
print("Tempo de Criação da Matriz:",execution_time)
print('MATRIZ CRIADA')
