def get_neighbors(grid, coord):
    x, y, rl, cl = coord[0], coord[1], len(grid), len(grid[0])
    return [(nx, ny) for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if ((0 <= nx < rl) and (0 <= ny < cl))]


def find_path(grid):
    stack = [
        (start, [start])
    ]
    # Stack holds the current position and the path taken to reach it
    visited = set()

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == destination:
            return path

        # Get neighbors and add valid ones to the stack
        for neighbor in get_neighbors(grid, current):
            x, y = neighbor
            if grid[x][y] == ____ and neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return []


start = (6, 6)
destination = (4, 6)
____ = "  "  # Path
wall = "XX"

# You can even edit the Maze, add few more rows and columns and make this a bit more complicated one.
maze = [  # Custom Maze
    #  0     1     2     3     4     5     6     7
    [wall, wall, wall, wall, wall, wall, wall, wall],  # 0
    [wall, ____, ____, ____, ____, ____, wall, wall],  # 1
    [wall, ____, wall, ____, wall, ____, wall, wall],  # 2
    [wall, ____, wall, ____, wall, ____, wall, wall],  # 3
    [wall, ____, wall, ____, wall, ____, ____, ____],  # 4
    [wall, ____, wall, ____, wall, wall, wall, ____],  # 5
    [wall, ____, wall, ____, ____, ____, ____, wall],  # 6
    [wall, wall, wall, wall, wall, wall, wall, wall],  # 7
]


path_ = find_path(maze)
if len(path_) == 0:
    print("No Path Found ! ")
for row in range(len(maze)):
    for col in range(len(maze[0])):
        if (row, col) in path_:
            print(f"\033[104m\033[94m{maze[row][col] if ((maze[row][col]).replace(' ', '')) != '' else '█'*len(maze[row][col])}\033[0m", end="")
        else:
            if maze[row][col] == wall:
                print("\033[30m\033[40m", end="")
            print(f"{maze[row][col]}\033[0m", end="")
    print()
