import pygame
import random

pygame.init()

class Maze:
    def __init__(self, gwidth, gheight):
        self.height = 1000
        self.width = 1000
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.run = True
        self.gwidth = gwidth
        self.gheight = gheight
        self.directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        self.position = [(1, 1)]
        self.generategrid()

        if self.width//self.gwidth > self.height//self.gheight:
            self.cell = self.height//self.gheight
        else:
            self.cell = self.width // self.gwidth

        self.entrance = (0, 1)
        self.exit = (self.gwidth - 2, self.gheight - 2)

    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.screen.fill((255, 255, 255))

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
                    self.maze[self.entrance[1]][self.entrance[0]] = 0
                    self.maze[-2][-1] = 0
                    if self.gwidth % 10 == 0 and self.gheight % 10 == 0:
                        self.maze[-2][-2] = 0
                        self.maze[-2][-3] = 0
                        self.maze[-3][-3] = 0
                        self.maze[-4][-3] = 0
                    elif self.gwidth % 10 == 0:
                        self.maze[-2][-2] = 0
                        self.maze[-2][-3] = 0



                    self.save_maze_to_file()
                    break

            self.draw()
            pygame.display.update()

    def draw(self):
        for x in range(self.gwidth):
            for y in range(self.gheight):
                if self.maze[y][x] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.cell, y * self.cell, self.cell, self.cell))
                elif self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * self.cell, y * self.cell, self.cell, self.cell))
                if y == len(self.maze) - 2 and x == len(self.maze[y]) - 1:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x * self.cell, y * self.cell, self.cell, self.cell))
                if (x, y) == self.entrance:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x * self.cell, y * self.cell, self.cell, self.cell))

    def generategrid(self):
        self.maze = [[1 for _ in range(self.gwidth)] for _ in range(self.gheight)]

    def is_valid(self, x, y):
        return (
                0 < x < self.gwidth - 1 and
                0 < y < self.gheight - 1 and
                self.maze[y][x] == 1
        )

    def save_maze_to_file(self):
        with open('maze.txt', "w") as f:
            for row in self.maze:
                f.write("".join(map(str, row)) + "\n")
        f.close()

        global screen
        screen = pygame.display.set_mode((self.width, self.height))

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            screen.fill((255, 255, 255))

            self.draw()
            pygame.display.update()

    def load_maze_from_file(self):
        with open('maze.txt', "r") as file:
            self.maze = [list(map(int, line.split())) for line in file]


if __name__ == "__main__":
    maze = Maze(41, 41)
    maze.mainloop()
