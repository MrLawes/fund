# Example file showing a circle moving on screen
import random
import time

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_pos_list = [player_pos, ]
player_pos_dict = {'1': player_pos}

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    for player_pos in player_pos_dict.values():
        pygame.draw.ellipse(screen, "red", (player_pos.x, player_pos.y, 50, 70))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        player_pos_dict[int(time.time())] = pygame.Vector2(random.randint(1, 1280), random.randint(1, 720))
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
