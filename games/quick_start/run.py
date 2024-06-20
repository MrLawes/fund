import random

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
IS_KEYDOWN = False
IS_KEYUP = False
screen.fill("purple")

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            IS_KEYDOWN = True
        elif event.type == pygame.KEYUP:
            IS_KEYUP = True
        if IS_KEYDOWN and IS_KEYUP:
            IS_KEYDOWN = False
            IS_KEYUP = False
            pygame.draw.ellipse(screen, "red", (random.randint(1, 1280), random.randint(1, 720), 50, 70))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
