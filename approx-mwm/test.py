def dfs(x, i, path):
    if i % 3 == 0:
        print(path)
    if i < len(x):
        dfs(x, i + 1, [*path, x[i]])
        print(f'done with {path}')

dfs(range(10), 0, [])