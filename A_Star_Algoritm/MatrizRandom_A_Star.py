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
    robot_position = random.choice(positions[num_ones:])
    product_position = random.choice(positions[num_ones:])

    while product_position[0]==robot_position[0] and product_position[1]==robot_position[1]:
        product_position = random.choice(positions[num_ones:])
        
    output_position = random.choice(positions[num_ones:])
    
    while output_position[0]==robot_position[0] and output_position[1]==robot_position[1] or output_position[0]==product_position[0] and output_position[1]==product_position[1]:
        product_position = random.choice(positions[num_ones:])

    matrix[robot_position[0]][robot_position[1]] = 'R'
    matrix[product_position[0]][product_position[1]] = 'P'
    matrix[output_position[0]][output_position[1]] = 'O'

    return matrix

# Cria a matriz
matrix = create_matrix(20, 20, 10, 10)

# Imprime a matriz alinhada
for row in matrix:
    print(' '.join(map(str, row)))

# Guarda a matriz em um arquivo txt identificado como "MatrixProcura"
#Ficheiro é gravado sem espaços para depois ser mais facil de ler e validar o BFS
with open("A_Star_Algoritm/MatrizRandom_A_Star.txt", "w") as file:
    for row in matrix:
        file.write(' '.join(row) + '\n')