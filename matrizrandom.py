import random

# Função para criar a matriz com a percentagem desejada de 1s e um ponto 'P'
def create_matrix(rows, cols, min_percentage, max_percentage):
    matrix = [['.' for _ in range(cols)] for _ in range(rows)]
    num_ones = random.randint(rows * cols * min_percentage // 100, rows * cols * max_percentage // 100)

    positions = [(i, j) for i in range(rows) for j in range(cols)]
    random.shuffle(positions)

    for i, j in positions[:num_ones]:
        matrix[i][j] = '#'

    # Adiciona 'R' e 'P' em posições aleatórias
    robot_position = (0, 0)  # Posição (1, 10)
    product_position = random.choice(positions[num_ones:])

    matrix[robot_position[0]][robot_position[1]] = 'R'
    matrix[product_position[0]][product_position[1]] = 'P'

    return matrix

# Cria a matriz
matrix = create_matrix(10, 10, 10, 30)

# Imprime a matriz alinhada
for row in matrix:
    print(' '.join(map(str, row)))

# Salva a matriz em um arquivo txt identificado como "PP"
with open("PP.txt", "w") as file:
    for row in matrix:
        file.write(' '.join(map(str, row)) + '\n')