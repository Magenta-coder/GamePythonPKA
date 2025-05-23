import pygame
import sys
import random
from collections import deque

from config import (WIDTH, HEIGHT, GRID_SIZE, CELL_WIDTH, CELL_HEIGHT, BG_DARK,
                    GRID_LINES, PATH_HINT, INFO_TEXT, FONT_SM, SCREEN)
from node import Node
from utils import bfs, generate_random_obstacles, generate_fruit
from screens import show_start_screen, show_end_screen


# --- Fungsi Utama Game (`game_loop`) ---
def game_loop():
    running = True
    while running:
        show_start_screen()

        grid = [[Node(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

        # Inisialisasi ular
        snake_head_x = GRID_SIZE // 2
        snake_head_y = GRID_SIZE // 2
        snake_body = deque([(snake_head_x, snake_head_y)])  # Deque untuk body ular

        grid[snake_head_y][snake_head_x].is_start = True  # Kepala ular
        grid[snake_head_y][snake_head_x].on_snake = True

        # Arah awal ular (default, akan diubah oleh pemain)
        dx, dy = 1, 0  # Arah awal, misalnya ke kanan

        # Generasi buah pertama
        current_fruit = generate_fruit(grid, list(snake_body))

        # Generasi obstacle (pastikan tidak menimpa kepala atau buah awal)
        safe_coords = [(snake_head_x, snake_head_y), (current_fruit.x, current_fruit.y)]
        NUM_OBSTACLES = random.randint(GRID_SIZE * GRID_SIZE // 15, GRID_SIZE * GRID_SIZE // 7)
        generate_random_obstacles(grid, NUM_OBSTACLES, safe_coords, buffer_zone=3)

        # Jalur petunjuk (hanya visualisasi)
        path_hint = []

        score = 0
        MAX_FRUITS = 10
        TIME_LIMIT = 60  # detik

        start_time = pygame.time.get_ticks()  # Waktu mulai game
        game_active = True
        game_won = False

        # Kecepatan gerakan ular (seberapa sering ular mencoba bergerak)
        game_speed_ms = 300  # milliseconds per frame (lebih besar = lebih lambat)
        last_move_time = pygame.time.get_ticks()

        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                    running = False
                # Perbaikan: event.type harus dibandingkan dengan pygame.KEYDOWN, bukan event.key dengan K_ESCAPE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Tombol ESC untuk keluar cepat
                        game_active = False
                        running = False
                    # Kontrol pemain dengan tombol panah
                    elif event.key == pygame.K_UP:
                        if dy != 1:  # Tidak bisa langsung balik arah
                            dx, dy = 0, -1
                    elif event.key == pygame.K_DOWN:
                        if dy != -1:
                            dx, dy = 0, 1
                    elif event.key == pygame.K_LEFT:
                        if dx != 1:
                            dx, dy = -1, 0
                    elif event.key == pygame.K_RIGHT:
                        if dx != -1:
                            dx, dy = 1, 0

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000  # dalam detik

            # Kondisi game berakhir
            if elapsed_time >= TIME_LIMIT:
                game_active = False
                game_won = False
                break
            if score >= MAX_FRUITS:
                game_active = False
                game_won = True
                break

            # --- Pergerakan Ular berdasarkan Kontrol Pemain ---
            if current_time - last_move_time > game_speed_ms:
                last_move_time = current_time

                new_head_x = snake_head_x + dx
                new_head_y = snake_head_y + dy

                # === Pengecekan Tabrakan ===
                if not (0 <= new_head_x < GRID_SIZE and 0 <= new_head_y < GRID_SIZE):
                    game_active = False;
                    game_won = False
                    print("Game Over: Menabrak dinding!")
                    break
                target_node = grid[new_head_y][new_head_x]
                if target_node.is_obstacle:
                    game_active = False;
                    game_won = False
                    print("Game Over: Menabrak obstacle!")
                    break
                if (new_head_x, new_head_y) in list(snake_body)[:-1]:
                    game_active = False;
                    game_won = False
                    print("Game Over: Menabrak tubuh sendiri!")
                    break

                # Update posisi kepala ular
                grid[snake_head_y][snake_head_x].is_start = False
                grid[snake_head_y][snake_head_x].on_snake = True
                snake_head_x = new_head_x
                snake_head_y = new_head_y
                grid[snake_head_y][snake_head_x].is_start = True
                grid[snake_head_y][snake_head_x].on_snake = True
                snake_body.appendleft((snake_head_x, snake_head_y))

                if snake_head_x == current_fruit.x and snake_head_y == current_fruit.y:
                    score += 1
                    current_fruit.is_end = False
                    current_fruit.on_snake = True
                    current_fruit = generate_fruit(grid, list(snake_body))
                    if game_speed_ms > 30: game_speed_ms -= 5
                else:
                    tail_x, tail_y = snake_body.pop()
                    grid[tail_y][tail_x].on_snake = False
                    grid[tail_y][tail_x].is_start = False
                    grid[tail_y][tail_x].is_end = False

                snake_head_node = grid[snake_head_y][snake_head_x]
                path_hint = bfs(snake_head_node, current_fruit, grid, list(snake_body)[1:])

            # --- Drawing ---
            SCREEN.fill(BG_DARK)
            for row in grid:
                for node_item in row:  # Ganti nama node menjadi node_item
                    node_item.draw(SCREEN)
            if path_hint:
                for node_item in path_hint:  # Ganti nama node menjadi node_item
                    if not node_item.is_start and not node_item.is_end and not node_item.on_snake:
                        pygame.draw.rect(SCREEN, PATH_HINT,
                                         (node_item.x * CELL_WIDTH, node_item.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT),
                                         0)
                        pygame.draw.rect(SCREEN, GRID_LINES,
                                         (node_item.x * CELL_WIDTH, node_item.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT),
                                         1)
            for x_s, y_s in snake_body:
                grid[y_s][x_s].draw(SCREEN)
            current_fruit.draw(SCREEN)
            score_text_render = FONT_SM.render(f"Buah: {score}/{MAX_FRUITS}", True, INFO_TEXT)
            time_text_render = FONT_SM.render(f"Waktu: {TIME_LIMIT - elapsed_time}s", True, INFO_TEXT)
            SCREEN.blit(score_text_render, (10, 10))
            SCREEN.blit(time_text_render, (WIDTH - time_text_render.get_width() - 10, 10))
            pygame.display.flip()

        play_again = show_end_screen(score, game_won)
        if not play_again:
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()