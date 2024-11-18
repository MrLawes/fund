import random

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
IS_KEYDOWN = False
IS_KEYUP = False
screen.fill((89, 181, 248))
pygame.draw.ellipse(screen, (67, 129, 179), (1145, 35, 70, 50,))
pygame.display.flip()
font = pygame.font.SysFont('songti', 16, False)
score = 0
surface = font.render(f'{score:>03}', False, "white")
screen.blit(surface, [1150 + 20, 30 + 20])

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            IS_KEYDOWN = True
        elif event.type == pygame.KEYUP:
            IS_KEYUP = True
        if IS_KEYDOWN and IS_KEYUP:
            IS_KEYUP = IS_KEYDOWN = False
            c1 = random.randint(0, 255)
            c2 = random.randint(0, 255)
            c3 = random.randint(0, 255)
            screen.fill((c1, c2, c3))
            for iii in range(0, score):
                rect = [random.randint(1, 1280), random.randint(1, 720), 50, 70]
                pygame.draw.ellipse(screen, "black", rect)
                rect[2] -= 5
                rect[3] -= 5
                rect[0] += 2
                rect[1] += 2
                c1 = random.randint(0, 255)
                c2 = random.randint(0, 255)
                c3 = random.randint(0, 255)
                pygame.draw.ellipse(screen, (c1, c2, c3), rect)
                # 下几个蛋 = 1
                # try:
                #     下几个蛋 = int(event.dict["unicode"])
                # except:
                #     pass
                # for i in range(0, 下几个蛋):
                #     c1 = random.randint(0, 255)
                #     c2 = random.randint(0, 255)
                #     c3 = random.randint(0, 255)
                #     pygame.draw.ellipse(screen, (c1, c2, c3), rect)
            score += 1
            # c1 = random.randint(0, 255)
            # c2 = random.randint(0, 255)
            # c3 = random.randint(0, 255)
            pygame.draw.ellipse(screen, (67, 129, 179), (1145, 35, 70, 50,))
            surface = font.render(f'{score:>03}', False, "white")
            screen.blit(surface, [1150 + 20, 30 + 20])

    pygame.display.flip()
    pygame.time.Clock().tick(60)
