import random
from collections import deque
from config import GRID_SIZE # Hanya import yang benar-benar dibutuhkan

# --- Fungsi Algoritma Pencarian Rute (BFS) ---
def bfs(start_node, end_node, grid, snake_body_coords):
    q = deque()
    # Reset visited dan parent untuk setiap pencarian BFS
    for row in grid:
        for node in row:
            node.visited = False
            node.parent = None

    q.append(start_node)
    start_node.visited = True

    found = False
    while q:
        current_node = q.popleft()

        if current_node == end_node:
            found = True
            break

        # Tetangga (atas, bawah, kiri, kanan)
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # dy, dx

        for dy, dx_move in possible_moves: # Ganti nama dx menjadi dx_move untuk menghindari konflik dengan parameter fungsi nanti
            nx, ny = current_node.x + dx_move, current_node.y + dy

            # Pastikan tetangga berada di dalam batas grid
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                neighbor = grid[ny][nx]
                # Pastikan tetangga bukan obstacle, belum dikunjungi, dan bukan bagian dari tubuh ular (kecuali ekor yang akan hilang)
                if not neighbor.is_obstacle and not neighbor.visited and (nx, ny) not in snake_body_coords:
                    neighbor.visited = True
                    neighbor.parent = current_node
                    q.append(neighbor)

    if found:
        # Rekonstruksi jalur
        path = []
        current = end_node
        while current is not None and current != start_node:  # Berhenti di start_node
            path.append(current)
            current = current.parent
        return path[::-1]  # Balik jalur agar dari start ke end (buah)
    return None


# --- Fungsi Utilitas Game ---
def reset_grid(grid):
    for row in grid:
        for node in row:
            node.is_obstacle = False
            node.is_start = False
            node.is_end = False
            node.parent = None
            node.visited = False
            node.on_snake = False


def generate_random_obstacles(grid, num_obstacles, safe_coords_list, buffer_zone=3):
    """
    Menghasilkan obstacle secara acak, menghindari zona aman.
    buffer_zone: Ukuran area persegi di sekitar setiap safe_coord yang harus dihindari.
    """
    forbidden_coords = set()
    for sx, sy in safe_coords_list:
        for x_offset in range(-buffer_zone, buffer_zone + 1):
            for y_offset in range(-buffer_zone, buffer_zone + 1):
                fx, fy = sx + x_offset, sy + y_offset
                if 0 <= fx < GRID_SIZE and 0 <= fy < GRID_SIZE:
                    forbidden_coords.add((fx, fy))

    obstacle_count = 0
    attempts = 0
    MAX_ATTEMPTS = num_obstacles * 5

    while obstacle_count < num_obstacles and attempts < MAX_ATTEMPTS:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        node = grid[y][x]

        if not node.is_obstacle and (x, y) not in forbidden_coords:
            node.is_obstacle = True
            obstacle_count += 1
        attempts += 1

    if attempts >= MAX_ATTEMPTS and obstacle_count < num_obstacles:
        print(f"Warning: Could not place all {num_obstacles} obstacles. Placed {obstacle_count}.")


def generate_fruit(grid, snake_body_coords):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        node = grid[y][x]
        if not node.is_obstacle and not (x, y) in snake_body_coords:
            node.is_end = True
            return node