import pygame
from board import boards
from collections import deque
import math
import random
import heapq
import black
import psutil  
import time

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
pygame.display.set_caption("Pacman")
fps = 60
color = 'blue'
PI = math.pi
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
counter = 0
flicker = False

player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'player_images/{i}.png'), (45, 45)))

class Blue_ghost:
    def __init__(self):
        self.num1 = ((HEIGHT - 50) // 32)  # Cell height
        self.num2 = (WIDTH // 30)           # Cell width
        self.image = pygame.image.load('ghost_images/blue.png')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.speed = 5  # Reduced speed for slower movement
        self.path = []  # Stores the path to follow
        self.count = 8
        self.target_x = 0
        self.target_y = 0
        self.time = 0 
        self.memory = 0
        self.set_initial_position()

    def set_initial_position(self):
        x = 14
        y = 6
        self.x = x * self.num2 + (0.5 * self.num2) - 22
        self.y = y * self.num1 + (0.5 * self.num1) - 22
        #while True:
        #    self.x = random.randint(0, 29)  # Random column
        #    self.y = random.randint(0, 31)  # Random row
        #    
        #    if level[self.y][self.x] == 1 or level[self.y][self.x] == 2 or level[self.y][self.x] == 10:  # Ensure the ghost starts on a valid path
        #        self.x = self.x * self.num2 + (0.5 * self.num2) - 22
        #        self.y = self.y * self.num1 + (0.5 * self.num1) - 22
        #        break

    def move(self):
        if not self.path:
            if self.count == 8:
                # If no path, calculate a new path to the player
                self.calculate_path_to_player()

            if self.count > 0:
                dx = self.target_x - self.x
                dy = self.target_y - self.y
                distance = math.hypot(dx, dy)
                if self.count == 1: 
                   self.x = self.target_x
                   self.y = self.target_y
                   self.count = 0
                else:
                    self.x += (dx / distance) * self.speed
                    self.y += (dy / distance) * self.speed
                    self.count -= 1

            if self.path:
                next_cell = self.path.pop(0)
                self.target_x = next_cell[0] * self.num2 + (0.5 * self.num2) - 22
                self.target_y = next_cell[1] * self.num1 + (0.5 * self.num1) - 22
        else:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y

                if self.path:
                    if len(self.path) == 1:
                        self.count -= 1                         
                    next_cell = self.path.pop(0)
                    self.target_x = next_cell[0] * self.num2 + (0.5 * self.num2) - 22
                    self.target_y = next_cell[1] * self.num1 + (0.5 * self.num1) - 22
            else:
                # Di chuyển từng bước nhỏ hướng về target
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        
    def calculate_path_to_player(self):
        # Convert ghost and player positions to grid coordinates
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)

        start_time = time.time() 
        mem_before = psutil.Process().memory_info().rss / 1024
        self.path = self.dfs((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))
        end_time = time.time() 
        mem_after = float(psutil.Process().memory_info().rss) / 1024
        self.time = end_time - start_time 
        self.memory = mem_after - mem_before

    def dfs(self, start, goal):
        stack = [(start, [])]  # Mỗi phần tử là ((x, y), path)
        visited = set()
        self.expanded_nodes = 0  

        while stack:
            (x, y), path = stack.pop()
            self.expanded_nodes += 1

            if (x, y) == goal:
                return path + [(x, y)]
        
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Duyệt các ô lân cận: lên, xuống, trái, phải
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 9 or level[ny][nx] == 10:  # Chỉ duyệt qua các ô hợp lệ
                        stack.append(((nx, ny), path + [(x, y)]))
        return []  # Không tìm thấy đường

    def draw_ghost(self):
        screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        
        x = 2
        y = 2
        self.x = x * num2 + (0.5 * num2) - 22
        self.y = y * num1 + (0.5 * num1) - 22
        #while True:
        #    self.x = random.randint(0, 29)  
        #    self.y = random.randint(0, 31)  
            
        #    if level[self.y][self.x] == 1 or level[self.y][self.x] == 2:
        #        self.x = self.x * num2 + (0.5 * num2) - 22
        #        self.y = self.y * num1 + (0.5 * num1) - 22
        #        break

    def draw_player(self):
        screen.blit(player_images[counter // 5], (self.x, self.y))

player = Player()
blue = Blue_ghost()

    

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)): 
        for j in range(len(level[i])):
            # if level[i][j] == 1:
            #     pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            # if level[i][j] == 2 and not flicker:
            #     pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    screen.fill('black')    
    draw_board()
    player.draw_player()
    blue.move()
    blue.draw_ghost()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Time:{blue.time:10f}s")
            print(f"Memory Usage: {blue.memory:.2f} KB")
            print(f"Expanded Nodes: {blue.expanded_nodes}")
            run = False
    
    pygame.display.flip()
pygame.quit() 