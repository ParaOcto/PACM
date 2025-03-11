from board import boards
from collections import deque
import time
import pygame
import math
import random
import heapq

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

def calculate_game_duration(start_time):
    return time.time() - start_time

class Ghost:
    def __init__(self, image_path, speed):
        self.num1 = ((HEIGHT - 50) // 32)  # Cell height
        self.num2 = (WIDTH // 30)           # Cell width
        self.image = pygame.transform.scale(pygame.image.load(image_path), (45, 45))
        self.speed = speed
        self.path = []
        self.move_delay = 30
        self.move_counter = 0
        self.set_initial_position()

    def set_initial_position(self):
        while True:
            self.x = random.randint(0, 29)
            self.y = random.randint(0, 31)
            
            if level[self.y][self.x] == 10:
                self.x = self.x * self.num2 + (0.5 * self.num2) - 22
                self.y = self.y * self.num1 + (0.5 * self.num1) - 22
                break

    def move(self):
        if self.move_counter >= self.move_delay:
            if not self.path:
                self.calculate_path_to_player()
            
            if self.path:
                next_x, next_y = self.path.pop(0)
                self.x = next_x * self.num2 + (0.5 * self.num2) - 22
                self.y = next_y * self.num1 + (0.5 * self.num1) - 22
            
            self.move_counter = 0
        else:
            self.move_counter += self.speed

    def draw_ghost(self):
        screen.blit(self.image, (self.x, self.y))

class Pink_ghost(Ghost):
    def __init__(self):
        super().__init__('ghost_images/pink.png', 4)
    
    def calculate_path_to_player(self):
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)
        
        self.path = self.find_path((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))
    
    def find_path(self, start, goal):
        return self.bfs(start, goal)
        
    def bfs(self, start, goal):
        queue = deque([(start, [])])
        visited = set()

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == goal:
                return path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 9 or level[ny][nx] == 10:
                        queue.append(((nx, ny), path + [(x, y)]))

        return []

class Blue_ghost(Ghost):
    def __init__(self):
        super().__init__('ghost_images/blue.png', 3)
    
    def calculate_path_to_player(self):
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)
        
        self.path = self.find_path((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))
    
    def find_path(self, start, goal):
        return self.dfs(start, goal)
        
    def dfs(self, start, goal):
        stack = [(start, [])]
        visited = set()

        while stack:
            (x, y), path = stack.pop()
        
            if (x, y) == goal:
                return path + [(x, y)]
        
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 9 or level[ny][nx] == 10:
                        stack.append(((nx, ny), path + [(x, y)]))
        return []

class Orange_ghost(Ghost):
    def __init__(self):
        super().__init__('ghost_images/orange.png', 3)
    
    def calculate_path_to_player(self):
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)
        
        self.path = self.find_path((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))
    
    def find_path(self, start, goal):
        return self.ucs(start, goal)
        
    def ucs(self, start, goal):
        queue = [(0, start, [])]
        visited = set()

        while queue:
            cost, (x, y), path = heapq.heappop(queue)

            if (x, y) == goal:
                return path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 10 or level[ny][nx] == 9:
                        heapq.heappush(queue, (cost + 1, (nx, ny), path + [(x, y)]))

        return []

class Player:
    def __init__(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        self.direction = 'right'
        self.speed = 2
        
        while True:
            self.x = random.randint(0, 29)  
            self.y = random.randint(0, 31)  
            
            if level[self.y][self.x] == 1 or level[self.y][self.x] == 2:
                self.x = self.x * num2 + (0.5 * num2) - 22
                self.y = self.y * num1 + (0.5 * num1) - 22
                break
        
    def draw_player(self):
        screen.blit(player_images[counter // 5], (self.x, self.y))
        
    def move(self):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

        self.check_collisions()

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        
        grid_x = int((self.x + 22) // num2)
        grid_y = int((self.y + 22) // num1)

        # Check if the next cell in the current direction is not a valid path
        if self.direction == 'up':
            if level[grid_y - 1][grid_x] != 1 and level[grid_y - 1][grid_x] != 2:
                self.y = grid_y * num1 + (0.5 * num1) - 22
        elif self.direction == 'down':
            if level[grid_y + 1][grid_x] != 1 and level[grid_y + 1][grid_x] != 2:
                self.y = grid_y * num1 + (0.5 * num1) - 22
        elif self.direction == 'left':
            if level[grid_y][grid_x - 1] != 1 and level[grid_y][grid_x - 1] != 2:
                self.x = grid_x * num2 + (0.5 * num2) - 22
        elif self.direction == 'right':
            if level[grid_y][grid_x + 1] != 1 and level[grid_y][grid_x + 1] != 2:
                self.x = grid_x * num2 + (0.5 * num2) - 22

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)): 
        for j in range(len(level[i])):
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
                
def check_collision(player, ghost):
    player_grid_x = int((player.x + 22) // (WIDTH // 30))
    player_grid_y = int((player.y + 22) // ((HEIGHT - 50) // 32))
    ghost_grid_x = int((ghost.x + 22) // (WIDTH // 30))
    ghost_grid_y = int((ghost.y + 22) // ((HEIGHT - 50) // 32))
    
    return player_grid_x == ghost_grid_x and player_grid_y == ghost_grid_y

def display_game_over():
    game_over_font = pygame.font.Font('freesansbold.ttf', 64)
    game_over_text = game_over_font.render('GAME OVER', True, 'red')
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

def display_duration(duration):
    duration_text = font.render(f'Duration: {round(float(duration), 2)} seconds', True, 'white')
    screen.blit(duration_text, (10, 10))

# Initialize game objects
player = Player()
ghosts = [
    Pink_ghost(),
    Blue_ghost(),
    Orange_ghost()
]

# Main game loop
run = True
game_over = False
start_time = time.time()

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
    
    # Update and draw player
    player.move()
    player.draw_player()
    
    # Update and draw ghosts
    for ghost in ghosts:
        ghost.move()
        ghost.draw_ghost()
    
    # Calculate and display duration
    duration = calculate_game_duration(start_time)
    display_duration(duration)
    
    # Check player-ghost collisions
    for ghost in ghosts:
        if check_collision(player, ghost):
            game_over = True
    
    # Handle game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.direction = 'up'
            elif event.key == pygame.K_s:
                player.direction = 'down'
            elif event.key == pygame.K_a:
                player.direction = 'left'
            elif event.key == pygame.K_d:
                player.direction = 'right'
    
    # Handle game over
    if game_over:
        display_game_over()
        run = False
    
    pygame.display.flip()

pygame.quit()