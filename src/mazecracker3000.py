import pygame

class MazeCRACKER3000:
    def __init__(self, maze_file):
        self.maze = []
        self.load_maze(maze_file)
        self.scale_factor = 20
        self.start = (0, 0)
        self.end = (len(self.maze) - 2, len(self.maze[0]) - 2)
        self.visited = set()
        self.correct_path = []

    def load_maze(self, maze_file):
        with open(maze_file, 'r') as file:
            for line in file:
                row = [int(cell) for cell in line.split()]
                self.maze.append(row)

    def is_valid(self, x, y):
        return 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0]) and self.maze[x][y] == 1 and (x, y) not in self.visited

    def dfs(self, x, y):
        if (x, y) == self.end:
            return True

        if self.is_valid(x, y):
            self.visited.add((x, y))
            if self.dfs(x + 1, y) or self.dfs(x - 1, y) or self.dfs(x, y + 1) or self.dfs(x, y - 1):
                self.correct_path.append((x, y))
                return True

        return False

    def find_path(self):
        self.dfs(*self.start)

    def display_maze(self):
        pygame.init()
        screen = pygame.display.set_mode((len(self.maze[0]) * self.scale_factor, len(self.maze) * self.scale_factor))
        # pygame.display.set_caption("MazeCRACKER3000")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for x in range(len(self.maze)):
                for y in range(len(self.maze[0])):
                    color = (255, 255, 255)
                    if (x, y) == self.start:
                        color = (0, 255, 0)
                    elif (x, y) == self.end:
                        color = (255, 0, 0)
                    elif (x, y) in self.correct_path:
                        color = (0, 0, 255)
                    elif self.maze[x][y] == 0:
                        color = (0, 0, 0)

                    pygame.draw.rect(screen, color, (y * self.scale_factor, x * self.scale_factor, self.scale_factor, self.scale_factor))

            pygame.display.update()

if __name__ == "__main__":
    maze_file = "maze.txt"
    mazecracker = MazeCRACKER3000(maze_file)
    mazecracker.find_path()
    mazecracker.display_maze()
