import pygame
import random

pygame.init()

class Maze:
    def __init__(self, width, height, cell):
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.run = True
        self.cell = cell
        self.gwidth = self.width // self.cell
        self.gheight = self.height // self.cell
        self.directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        self.position = [(0, 0)]
        self.generategrid()

        self.entrance = (0, 0)
        self.exit = (self.gwidth - 2, self.gheight - 2)

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.screen.fill((0, 0, 0))

            current_x, current_y = self.position[-1]
            self.maze[current_y][current_x] = 0

            random.shuffle(self.directions)

            for dx, dy in self.directions:
                new_x, new_y = current_x + dx, current_y + dy
                if self.is_valid(new_x, new_y) and self.maze[new_y][new_x] == 1:
                    self.maze[current_y + dy // 2][current_x + dx // 2] = 0
                    self.position.append((new_x, new_y))
                    break
            else:
                if len(self.position) > 1:
                    self.position.pop()
                else:
                    self.save_maze_to_file()

            self.draw()
            pygame.display.update()

    def draw(self):
        for x in range(self.gwidth):
            for y in range(self.gheight):
                if self.maze[y][x] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.cell, y * self.cell, self.cell, self.cell))
                if (x, y) == self.entrance:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x * self.cell, y * self.cell, self.cell, self.cell))
                if (x, y) == self.exit:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x * self.cell, y * self.cell, self.cell, self.cell))


    def generategrid(self):
        self.maze = [[1 for _ in range(self.gwidth)] for _ in range(self.gheight)]

    def is_valid(self, x, y):
        return 0 <= x < self.gwidth and 0 <= y < self.gheight

    def save_maze_to_file(self):
        with open('maze.txt', "w") as f:
            for row in self.maze:
                f.write(" ".join(map(str, row)) + "\n")
        f.close()

    def load_maze_from_file(self):
        with open('maze.txt', "r") as file:
            self.maze = [list(map(int, line.split())) for line in file]


if __name__ == "__main__":
    maze = Maze(800, 800, 20)
    maze.mainloop()
