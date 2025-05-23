import pygame
import sys
from config import (SCREEN, BG_DARK, INFO_TEXT, LIGHT_GREY, GAME_WON_GREEN,
                    GAME_OVER_RED, FONT_LG, FONT_MD, FONT_SM, WIDTH, HEIGHT)

def show_start_screen():
    start_screen_running = True
    while start_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen_running = False

        SCREEN.fill(BG_DARK)
        title_text = FONT_LG.render("ULAR PENCARI RUTE", True, INFO_TEXT)
        play_text = FONT_MD.render("Tekan SPASI untuk Mulai", True, LIGHT_GREY)
        controls_text = FONT_SM.render("Kontrol: Panah Atas/Bawah/Kiri/Kanan", True, LIGHT_GREY)
        goal_text = FONT_SM.render("Tujuan: Makan 10 Buah dalam 60 Detik!", True, INFO_TEXT)

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        goal_rect = goal_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(play_text, play_rect)
        SCREEN.blit(controls_text, controls_rect)
        SCREEN.blit(goal_text, goal_rect)
        pygame.display.flip()


def show_end_screen(score, win):
    end_screen_running = True
    while end_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Play again
                    return True
                if event.key == pygame.K_q:  # Quit
                    return False

        SCREEN.fill(BG_DARK)

        if win:
            result_text = FONT_LG.render("ANDA MENANG!", True, GAME_WON_GREEN)
        else:
            result_text = FONT_LG.render("ANDA KALAH!", True, GAME_OVER_RED)

        score_text = FONT_MD.render(f"Buah Dimakan: {score}", True, INFO_TEXT)
        restart_text = FONT_SM.render("Tekan 'R' untuk Main Lagi", True, LIGHT_GREY)
        quit_text = FONT_SM.render("Tekan 'Q' untuk Keluar", True, LIGHT_GREY)

        result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

        SCREEN.blit(result_text, result_rect)
        SCREEN.blit(score_text, score_rect)
        SCREEN.blit(restart_text, restart_rect)
        SCREEN.blit(quit_text, quit_rect)
        pygame.display.flip()