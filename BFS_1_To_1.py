def solve(start_row, start_col):
    q = []
    q.append((start_row, start_col))
    visited = [[False for i in range(cols)] for j in range(rows)]
    visited[start_row][start_col] = True

    prev = [[None for i in range(cols)] for j in range(rows)]
    while len(q) > 0:
        row, col = q.pop(0)
        if matrizProcura[row][col] == 'P':
            return prev
        
        # Check adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr
            next_col = col + dc
            if (
                next_row >= 0 and next_row < rows and
                next_col >= 0 and next_col < cols and
                not visited[next_row][next_col] and
                matrizProcura[next_row][next_col] != '#'
            ):
                q.append((next_row, next_col))
                visited[next_row][next_col] = True
                prev[next_row][next_col] = (row, col)

    return None

def reconstructPath(start_row, start_col, end_row, end_col, prev):
    path = []
    row, col = end_row, end_col
    while (row, col) != (start_row, start_col):
        path.append((row, col))
        row, col = prev[row][col]
    path.append((start_row, start_col))
    path.reverse()
    return path

def bfs(start_row, start_col, end_row, end_col):
    prev = solve(start_row, start_col)
    if prev is None:
        print("Caminho não encontrado.")
        return []
    return reconstructPath(start_row, start_col, end_row, end_col, prev)


#Abrir o Ficheiro e ler todas as linhas
with open('MatrizRandom_BFS_1_To_1.txt', 'r') as f:
    matrizProcura = [linha.strip().split() for linha in f]


rows = len(matrizProcura)
cols = len(matrizProcura[0])
start_row = 0
start_col = 0
end_row = 0
end_col = 0

for i in range(rows):
    for j in range(cols):
        if matrizProcura[i][j] == 'R':
            start_row = i
            start_col = j
        if matrizProcura[i][j] == 'P':
            end_row = i
            end_col = j

print("Labirinto:")
for row in matrizProcura:
    print(' '.join(row))

print("\Procura do caminho um caminho:")

path = bfs(start_row, start_col, end_row, end_col)

if len(path) > 0:
    print("Caminho encontrado:")
    for row, col in path:
        if matrizProcura[row][col] != 'P':  
            matrizProcura[row][col] = 'R'
    for row in matrizProcura:
        print(' '.join(row))
    with open("MatrizRandom_BFS_1_To_1_OUTPUT.txt", "w") as file:
        for row in matrizProcura:
            file.write(' '.join(row) + '\n')
else:
    print("Caminho não encontrado.")


