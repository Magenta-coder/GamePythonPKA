import pygame
import sys
import heapq
import random
import time

pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
GRID_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Evakuasi Bencana")

WHITE = (245, 245, 255)
BLACK = (30, 30, 30)
RED = (200, 0, 0)
BLUE = (30, 144, 255)
GREEN = (0, 255, 127)
GREY = (211, 211, 211)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (148, 0, 211)
LIGHT_GREY = (230, 230, 250)
DARK_GREY = (169, 169, 169)

FONT = pygame.font.SysFont('arial', 18)
BIG_FONT = pygame.font.SysFont('arial', 32, bold=True)
SCORE_FONT = pygame.font.SysFont('comicsansms', 24, bold=True)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.color = WHITE
        self.neighbors = []
        self.blocked = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].blocked:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].blocked:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].blocked:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].blocked:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

def make_grid():
    return [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(WIN, LIGHT_GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(WIN, LIGHT_GREY, (0, y), (WIDTH, y))

def draw(win, grid, score, elapsed_time):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid()
    pygame.draw.rect(win, DARK_GREY, (0, 0, WIDTH, 35))
    score_text = SCORE_FONT.render(f"👥 Warga Selamat: {score}", True, WHITE)
    time_text = FONT.render(f"⏱️ Waktu: {elapsed_time:.1f} detik", True, WHITE)
    win.blit(score_text, (10, 5))
    win.blit(time_text, (250, 10))
    pygame.display.update()

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def a_star_path(grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start, end)
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return []

def random_block(grid, start_points, end_points):
    for row in grid:
        for node in row:
            if random.random() < 0.1 and node not in start_points and node not in end_points:
                node.blocked = True
                node.color = BLACK

def animate_disaster(grid):
    for _ in range(10):
        for _ in range(5):
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            node = grid[r][c]
            if node.color == WHITE:
                node.blocked = True
                node.color = RED
        draw(WIN, grid, 0, 0)
        pygame.time.delay(300)

def start_menu():
    WIN.fill(BLUE)
    title = BIG_FONT.render("Simulasi Evakuasi Bencana", True, WHITE)
    play = FONT.render("Tekan [ENTER] untuk Memulai", True, WHITE)
    quit_game = FONT.render("Tekan [ESC] untuk Keluar", True, WHITE)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    WIN.blit(play, (WIDTH//2 - play.get_width()//2, HEIGHT//2))
    WIN.blit(quit_game, (WIDTH//2 - quit_game.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_result(score, total, elapsed_time):
    WIN.fill(WHITE)
    result = BIG_FONT.render("Simulasi Selesai", True, BLUE)
    count_text = FONT.render(f"Jumlah Warga: {total}", True, BLACK)
    score_text = FONT.render(f"Warga Selamat: {score}", True, BLACK)
    stuck_text = FONT.render(f"Warga Terjebak: {total - score}", True, BLACK)
    retry_text = FONT.render("Ingin bermain lagi? Tekan [Y]a / [T]idak", True, BLACK)
    WIN.blit(result, (WIDTH//2 - result.get_width()//2, HEIGHT//3))
    WIN.blit(count_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    WIN.blit(score_text, (WIDTH//2 - stuck_text.get_width()//2, HEIGHT//2 + 30))
    WIN.blit(stuck_text, (WIDTH//2 - stuck_text.get_width()//2, HEIGHT//2 + 60))
    WIN.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2 + 100))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    main()
                elif event.key == pygame.K_t:
                    pygame.quit()
                    sys.exit()

def main():
    start_menu()
    start_points = []
    end_points = []
    people = []
    score = 0
    grid = make_grid()
    random_block(grid, start_points, end_points)
    animate_disaster(grid)
    start_time = time.time()
    running = True

    while running:
        elapsed_time = time.time() - start_time
        draw(WIN, grid, score, elapsed_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                row, col = y // GRID_SIZE, x // GRID_SIZE
                node = grid[row][col]
                if node not in start_points and node not in end_points:
                    node.color = ORANGE
                    start_points.append(node)
                    people.append({"pos": node, "path": [], "reached": False})

            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                row, col = y // GRID_SIZE, x // GRID_SIZE
                node = grid[row][col]
                if node in start_points:
                    start_points.remove(node)
                if node in end_points:
                    end_points.remove(node)
                node.color = WHITE
                node.blocked = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // GRID_SIZE, x // GRID_SIZE
                    node = grid[row][col]
                    if node not in end_points and node not in start_points:
                        node.color = YELLOW
                        end_points.append(node)

                if event.key == pygame.K_SPACE and start_points and end_points:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    for person in people:
                        shortest_path = None
                        for end in end_points:
                            path = a_star_path(grid, person["pos"], end)
                            if not shortest_path or (path and len(path) < len(shortest_path)):
                                shortest_path = path
                        person["path"] = shortest_path

        for person in people:
            if not person["reached"] and person["path"]:
                next_node = person["path"].pop(0)
                person["pos"].color = ORANGE
                next_node.color = GREEN
                person["pos"] = next_node
                if next_node in end_points or not person["path"]:
                    person["reached"] = True
                    score += 1
            pygame.time.delay(20)

        # ⏰ Jika waktu simulasi mencapai detik yang ditentukan
        if elapsed_time >= 20:
            show_result(score, len(people), elapsed_time)
            running = False

main()