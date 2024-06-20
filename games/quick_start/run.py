import random

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(1280 / 2, 720 / 2)
player_pos_list = [player_pos, ]

IS_KEYDOWN = False
IS_KEYUP = False

while running:

    screen.fill("purple")

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            IS_KEYDOWN = True
        elif event.type == pygame.KEYUP:
            IS_KEYUP = True
        if IS_KEYDOWN and IS_KEYUP:
            IS_KEYDOWN = False
            IS_KEYUP = False
            player_pos_list.append(pygame.Vector2(random.randint(1, 1280), random.randint(1, 720)))

    for player_pos in player_pos_list:
        pygame.draw.ellipse(screen, "red", (player_pos.x, player_pos.y, 50, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
