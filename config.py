import pygame

# --- Konfigurasi Game ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40  # Ukuran setiap sel grid
CELL_WIDTH = WIDTH // GRID_SIZE
CELL_HEIGHT = HEIGHT // GRID_SIZE

# Warna (Palet "Soft & Vibrant")
BG_DARK = (28, 30, 33)
GRID_LINES = (50, 55, 60)
EMPTY_CELL = (40, 44, 48)
OBSTACLE_COLOR = (227, 208, 149) # Anda mengganti warna ini di kode Anda
LIGHT_GREY = (100, 100, 100)

SNAKE_HEAD = (82, 217, 126)
SNAKE_BODY = (50, 180, 90)

FRUIT_COLOR = (255, 99, 132)

PATH_HINT = (140, 200, 255)

INFO_TEXT = (255, 255, 200)
GAME_OVER_RED = (230, 70, 70)
GAME_WON_GREEN = (60, 190, 100)

# Inisialisasi Font (dipindahkan ke sini agar bisa diakses global jika perlu)
pygame.init() # Inisialisasi Pygame diperlukan sebelum font
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 36)
FONT_LG = pygame.font.Font(None, 48)

# Inisialisasi Layar Utama (juga bisa di sini)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Pencari Rute (Kontrol Pemain Penuh)")