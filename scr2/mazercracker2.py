import pygame

LIGHT_GRAY = (240, 239, 244)
RED = (201, 112, 100)
DARK_GRAY = (83, 86, 87)

f = open("maze.txt", "r")
lines = 0
maze = []
START_Y = 0
END_Y = 0
for line in f:
    maze.append(list(line.strip()))
    if line[0] == '0':
        START_Y = lines
    if maze[lines][-1] == '0':
        END_Y = lines
    lines += 1

MAX_WIDTH = 1000
MAX_HEIGHT = 1000

TILE_SIZE = 50

scale_factor = min(MAX_WIDTH / (len(maze[0]) * TILE_SIZE), MAX_HEIGHT / (len(maze) * TILE_SIZE))

WIDTH = min(int(len(maze[0]) * TILE_SIZE * scale_factor), MAX_WIDTH)
HEIGHT = min(int(len(maze) * TILE_SIZE * scale_factor), MAX_HEIGHT)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return f'(x: {self.x}, y: {self.y})'

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    def __str__(self):
        return f"{self.position}"

def getNeighbours(maze, x, y, parentNode, closed_nodes):
    neighbors = []
    height, width = len(maze), len(maze[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < height and 0 <= new_y < width and maze[new_y][new_x] == '0':
            if Node(parentNode, Point(new_x, new_y)) not in closed_nodes:
                neighbors.append(Node(parentNode, Point(new_x, new_y)))

    return neighbors

def drawGrid(TILE_SIZE, WIDTH, HEIGHT):
    for x in range(0, WIDTH, int(TILE_SIZE * scale_factor)):
        for y in range(0, HEIGHT, int(TILE_SIZE * scale_factor)):
            if maze[int(y / (TILE_SIZE * scale_factor))][int(x / (TILE_SIZE * scale_factor))] == '1':
                rect = pygame.Rect(x, y, int(TILE_SIZE * scale_factor), int(TILE_SIZE * scale_factor))
                pygame.draw.rect(screen, DARK_GRAY, rect)
            else:
                rect = pygame.Rect(x, y, int(TILE_SIZE * scale_factor), int(TILE_SIZE * scale_factor))
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)

def drawLine(TILE_SIZE,path):
    circle_radius = int(0.3 * TILE_SIZE * scale_factor)
    for point in path:
        x, y = point.x, point.y
        x_pixel = x * TILE_SIZE * scale_factor + 0.5 * TILE_SIZE * scale_factor
        y_pixel = y * TILE_SIZE * scale_factor + 0.5 * TILE_SIZE * scale_factor
        pygame.draw.circle(screen, RED, (int(x_pixel), int(y_pixel)), circle_radius)

def pathFind(start, end):
    open_paths = []
    closed_paths = []

    startNode = Node(None, Point(0, start))
    endNode = Node(None, Point(len(maze[0]) - 1, end))

    open_paths.append(startNode)

    while len(open_paths) > 0:
        currentNode = open_paths[0]
        currentIndex = 0

        for index, node in enumerate(open_paths):
            if node.f < currentNode.f:
                currentNode = node
                currentIndex = index

        open_paths.pop(currentIndex)
        closed_paths.append(currentNode)

        if currentNode.position == endNode.position:
            current = currentNode
            path = []
            while current is not None:
                path.insert(0, current.position)
                current = current.parent
            return path

        children = getNeighbours(maze, currentNode.position.x, currentNode.position.y, currentNode, closed_paths)

        for child in children:
            if child in closed_paths:
                continue

            child.g = currentNode.g + 1
            child.h = pow(endNode.position.y - child.position.y, 2) + pow(endNode.position.x - child.position.x, 2)
            child.f = child.g + child.h

            if child in open_paths:
                continue

            open_paths.append(child)

running = True

if HEIGHT - 1 > END_Y > 0 and HEIGHT - 1 > START_Y > 0:
    path = pathFind(START_Y, END_Y)
else:
    print("No solutions exist!")
msgShown = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(LIGHT_GRAY)

    drawGrid(TILE_SIZE, WIDTH, HEIGHT)
    if path is not None:
        drawLine(TILE_SIZE, path)
    else:
        if not msgShown:
            print("No solutions exist!")
            msgShown = True

    pygame.display.update()
