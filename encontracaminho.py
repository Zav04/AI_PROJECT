# def solve(start_row, start_col):
#     q = []
#     q.append((start_row, start_col))
#     visited = [[False for i in range(cols)] for j in range(rows)]
#     visited[start_row][start_col] = True

#     prev = [[None for i in range(cols)] for j in range(rows)]
#     while len(q) > 0:
#         row, col = q.pop(0)
#         if m[row][col] == 'P':
#             return prev
        
#         # Check adjacent cells
#         for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             next_row = row + dr
#             next_col = col + dc
#             if (
#                 next_row >= 0 and next_row < rows and
#                 next_col >= 0 and next_col < cols and
#                 not visited[next_row][next_col] and
#                 m[next_row][next_col] != '#'
#             ):
#                 q.append((next_row, next_col))
#                 visited[next_row][next_col] = True
#                 prev[next_row][next_col] = (row, col)

#     return None

# def reconstructPath(start_row, start_col, end_row, end_col, prev):
#     path = []
#     row, col = end_row, end_col
#     while (row, col) != (start_row, start_col):
#         path.append((row, col))
#         row, col = prev[row][col]
#     path.append((start_row, start_col))
#     path.reverse()
#     return path

# def bfs(start_row, start_col, end_row, end_col):
#     prev = solve(start_row, start_col)
#     if prev is None:
#         print("Caminho não encontrado.")
#         return []
#     return reconstructPath(start_row, start_col, end_row, end_col, prev)

# m = [
#     ['R', '.', '.', '.', '.', '.', '#', '#', '#' , '.'],
#     ['.', '.', '#', '.', '.', '.', '.', '.', '.' , '.'],
#     ['.', '.', '.', '#', '.', '.', '.', '#', '.' , '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.' , '#'],
#     ['.', '.', '.', '#', '.', '.', '.', '.', '.' , '.'],
#     ['#', '#', '.', '.', '#', '#', '.', '.', '#' , '.'],
#     ['.', '.', '.', '#', '#', '.', '.', '.', '.' , '.'],
#     ['P', '.', '.', '.', '.', '#', '.', '.', '.' , '.'],
#     ['#', '#', '#', '#', '.', '.', '.', '.', '.' , '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.' , '.'],
# ]

# rows = len(m)
# cols = len(m[0])
# start_row = 0
# start_col = 0
# end_row = 0
# end_col = 0

# for i in range(rows):
#     for j in range(cols):
#         if m[i][j] == 'S':
#             start_row = i
#             start_col = j
#         if m[i][j] == 'P':
#             end_row = i
#             end_col = j

# print("Labirinto:")
# for row in m:
#     print(' '.join(row))

# print("\nBuscando um caminho:")

# path = bfs(start_row, start_col, end_row, end_col)

# if len(path) > 0:
#     print("Caminho encontrado:")
#     for row, col in path:
#         m[row][col] = 'R'
#     for row in m:
#         print(' '.join(row))
# else:
#     print("Caminho não encontrado.")



def solve(start_row, start_col):
    q = []
    q.append((start_row, start_col))
    visited = [[False for i in range(cols)] for j in range(rows)]
    visited[start_row][start_col] = True

    prev = [[None for i in range(cols)] for j in range(rows)]
    while len(q) > 0:
        row, col = q.pop(0)
        if m[row][col] == 'P':
            return prev
        
        # Check adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr
            next_col = col + dc
            if (
                next_row >= 0 and next_row < rows and
                next_col >= 0 and next_col < cols and
                not visited[next_row][next_col] and
                m[next_row][next_col] != '#'
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

with open('PP.txt', 'r') as f:
    lines = f.read().splitlines()
    m = [list(line) for line in lines]

rows = len(m)
cols = len(m[0])
start_row = 0
start_col = 0
end_row = 0
end_col = 0

for i in range(rows):
    for j in range(cols):
        if m[i][j] == 'S':
            start_row = i
            start_col = j
        if m[i][j] == 'P':
            end_row = i
            end_col = j

print("Labirinto:")
for row in m:
    print(' '.join(row))

print("\nBuscando um caminho:")

path = bfs(start_row, start_col, end_row, end_col)

if len(path) > 0:
    print("Caminho encontrado:")
    for row, col in path:
        m[row][col] = 'R'
    for row in m:
        print(' '.join(row))
else:
    print("Caminho não encontrado.")


