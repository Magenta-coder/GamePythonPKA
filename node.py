import pygame
from config import (EMPTY_CELL, OBSTACLE_COLOR, FRUIT_COLOR, SNAKE_BODY,
                    SNAKE_HEAD, CELL_WIDTH, CELL_HEIGHT, GRID_LINES)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_obstacle = False
        self.is_start = False  # Sekarang ini hanya menandakan kepala ular
        self.is_end = False  # Menandakan buah
        self.parent = None  # Untuk melacak jalur BFS
        self.visited = False  # Untuk BFS
        self.on_snake = False  # Menandakan apakah node ini bagian dari ular

    def draw(self, screen):
        color = EMPTY_CELL  # Sel kosong
        if self.is_obstacle:
            color = OBSTACLE_COLOR
        elif self.is_end:  # Buah
            color = FRUIT_COLOR
        elif self.on_snake:
            color = SNAKE_BODY  # Bagian tubuh ular
        elif self.is_start:
            color = SNAKE_HEAD  # Kepala ular

        pygame.draw.rect(screen, color, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 0)
        pygame.draw.rect(screen, GRID_LINES, (self.x * CELL_WIDTH, self.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT),
                         1)  # Border