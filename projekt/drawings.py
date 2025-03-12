import pygame
import math


def draw_board(level, screen, color, cell_height, cell_width):

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * cell_width + (0.5 * cell_width), i * cell_height + (0.5 * cell_height)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * cell_width + (0.5 * cell_width), i * cell_height + (0.5 * cell_height)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * cell_width + (0.5 * cell_width), i * cell_height),
                                 (j * cell_width + (0.5 * cell_width), i * cell_height + cell_height), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * cell_width, i * cell_height + (0.5 * cell_height)),
                                 (j * cell_width + cell_width, i * cell_height + (0.5 * cell_height)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * cell_width - (cell_width * 0.4)) - 2, (i * cell_height + (0.5 * cell_height)), cell_width, cell_height],
                                0, math.pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * cell_width + (cell_width * 0.5)), (i * cell_height + (0.5 * cell_height)), cell_width, cell_height], math.pi / 2, math.pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * cell_width + (cell_width * 0.5)), (i * cell_height - (0.4 * cell_height)), cell_width, cell_height], math.pi,
                                3 * math.pi / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * cell_width - (cell_width * 0.4)) - 2, (i * cell_height - (0.4 * cell_height)), cell_width, cell_height], 3 * math.pi / 2,
                                2 * math.pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * cell_width, i * cell_height + (0.5 * cell_height)),
                                 (j * cell_width + cell_width, i * cell_height + (0.5 * cell_height)), 3)
                



def text(font, score, screen, eaten_ghost_counter):
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 600))
    
    eaten_ghost_text = font.render(f"Zjedzone duszki: {eaten_ghost_counter}", True, 'white')
    screen.blit(eaten_ghost_text, (300, 600))

