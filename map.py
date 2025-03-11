import pygame
from board import boards
import math
import random
from collections import deque
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

class Pink_ghost:
    def __init__(self):
        self.num1 = ((HEIGHT - 50) // 32)  # Cell height
        self.num2 = (WIDTH // 30)           # Cell width
        self.image = pygame.image.load('ghost_images/pink.png')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.speed = 3  # Reduced speed for slower movement
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.path = []  # Stores the path to follow
        self.count = 8
        self.target_x = 0
        self.target_y = 0
        self.move_delay = 30  # Delay between movements (frames)
        self.move_counter = 0
        self.set_initial_position()

    def set_initial_position(self):
        while True:
            self.x = random.randint(0, 29)  # Random column
            self.y = random.randint(0, 31)  # Random row
            
            if level[self.y][self.x] == 10:  # Ensure the ghost starts on a valid path
                self.x = self.x * self.num2 + (0.5 * self.num2) - 22
                self.y = self.y * self.num1 + (0.5 * self.num1) - 22
                break

    def move(self):
        if self.move_counter >= self.move_delay:
            if not self.path:
                # If no path, calculate a new path to the player
                self.calculate_path_to_player()
            
            if self.path:
                # Move to the next cell in the path
                next_x, next_y = self.path.pop(0)
                self.x = next_x * self.num2 + (0.5 * self.num2) - 22
                self.y = next_y * self.num1 + (0.5 * self.num1) - 22
            
            self.move_counter = 0  # Reset the counter after moving
        else:
            self.move_counter += self.speed  # Increment the counter
    def calculate_path_to_player(self):
        # Convert ghost and player positions to grid coordinates
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)

        # Use BFS to find the shortest path
        self.path = self.bfs((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))
        
    def bfs(self, start, goal):
        # Queue: ((x, y), path)
        queue = deque([(start, [])])
        visited = set()

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == goal:
                return path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Explore neighbors (Up, Down, Left, Right)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 9 or level[ny][nx] == 10:  # Valid path
                        queue.append(((nx, ny), path + [(x, y)]))

        return []  # No path found

    def draw_ghost(self):
        screen.blit(self.image, (self.x, self.y))

class Blue_ghost:
    def __init__(self):
        self.num1 = ((HEIGHT - 50) // 32)  # Cell height
        self.num2 = (WIDTH // 30)           # Cell width
        self.image = pygame.image.load('ghost_images/blue.png')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.speed = 3 # Reduced speed for slower movement
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.path = []  # Stores the path to follow
        self.count = 8
        self.move_delay = 30  # Delay between movements (frames)
        self.target_x = 0
        self.target_y = 0
        self.move_counter = 0
        self.set_initial_position()

    def set_initial_position(self):
        while True:
            self.x = random.randint(0, 29)  # Random column
            self.y = random.randint(0, 31)  # Random row
            
            if level[self.y][self.x] == 10:  # Ensure the ghost starts on a valid path
                self.x = self.x * self.num2 + (0.5 * self.num2) - 22
                self.y = self.y * self.num1 + (0.5 * self.num1) - 22
                break

    def move(self):
        if self.move_counter >= self.move_delay:
            if not self.path:
                # If no path, calculate a new path to the player
                self.calculate_path_to_player()
            
            if self.path:
                # Move to the next cell in the path
                next_x, next_y = self.path.pop(0)
                self.x = next_x * self.num2 + (0.5 * self.num2) - 22
                self.y = next_y * self.num1 + (0.5 * self.num1) - 22
            
            self.move_counter = 0  # Reset the counter after moving
        else:
            self.move_counter += self.speed  # Increment the counter

        
    def calculate_path_to_player(self):
        # Convert ghost and player positions to grid coordinates
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)

        # Use DFS to find the shortest path
        self.path = self.dfs((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))

    def dfs(self, start, goal):
        stack = [(start, [])]  # Mỗi phần tử là ((x, y), path)
        visited = set()

        while stack:
            (x, y), path = stack.pop()
        
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

class Orange_ghost:
    def __init__(self):
        self.num1 = ((HEIGHT - 50) // 32)  # Cell height
        self.num2 = (WIDTH // 30)           # Cell width
        self.image = pygame.image.load('ghost_images/orange.png')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.speed = 3  # Reduced speed for slower movementg
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.path = []  # Stores the path to follow
        self.move_delay = 30  # Delay between movements (frames)
        self.move_counter = 0  # Counter to track movement delay
        self.set_initial_position()

    def set_initial_position(self):
        while True:
            self.x = random.randint(0, 29)  # Random column
            self.y = random.randint(0, 31)  # Random row
            
            if level[self.y][self.x] == 10: # or level[self.y][self.x] == 2:   Ensure the ghost starts on a valid path
                self.x = self.x * self.num2 + (0.5 * self.num2) - 22
                self.y = self.y * self.num1 + (0.5 * self.num1) - 22
                break

    def move(self):
        if self.move_counter >= self.move_delay:
            if not self.path:
                # If no path, calculate a new path to the player
                self.calculate_path_to_player()
            
            if self.path:
                # Move to the next cell in the path
                next_x, next_y = self.path.pop(0)
                self.x = next_x * self.num2 + (0.5 * self.num2) - 22
                self.y = next_y * self.num1 + (0.5 * self.num1) - 22
            
            self.move_counter = 0  # Reset the counter after moving
        else:
            self.move_counter += self.speed  # Increment the counter

    def calculate_path_to_player(self):
        # Convert ghost and player positions to grid coordinates
        ghost_grid_x = int((self.x + 22) // self.num2)
        ghost_grid_y = int((self.y + 22) // self.num1)
        player_grid_x = int((player.x + 22) // self.num2)
        player_grid_y = int((player.y + 22) // self.num1)

        # Use UCS to find the shortest path
        self.path = self.ucs((ghost_grid_x, ghost_grid_y), (player_grid_x, player_grid_y))

    def ucs(self, start, goal):
        # Priority queue: (cost, (x, y), path)
        queue = [(0, start, [])]
        visited = set()

        while queue:
            cost, (x, y), path = heapq.heappop(queue)

            if (x, y) == goal:
                return path + [(x, y)]

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Explore neighbors
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Up, Down, Left, Right
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == 1 or level[ny][nx] == 2 or level[ny][nx] == 10 or level[ny][nx] == 9:  # Valid path
                        heapq.heappush(queue, (cost + 1, (nx, ny), path + [(x, y)]))

        return []  # No path found

    def draw_ghost(self):
        screen.blit(self.image, (self.x, self.y))

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

        # Check if the next cell in the current direction is not a direction
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

player = Player()
orange = Orange_ghost()
blue = Blue_ghost()
pink = Pink_ghost()
    

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)): 
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
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
    player.move()
    player.draw_player()
    orange.move()
    orange.draw_ghost()
    blue.move()
    blue.draw_ghost()   
    pink.move()
    pink.draw_ghost()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move up
                player.direction = 'up'
            elif event.key == pygame.K_s:  # Move down
                player.direction = 'down'
            elif event.key == pygame.K_a:  # Move left
                player.direction = 'left'
            elif event.key == pygame.K_d:  # Move right
                player.direction = 'right'
    
    pygame.display.flip()
pygame.quit() 