# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_pos_2 = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_pos_3 = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")
    # screen.fill("purple")

    pygame.draw.circle(screen, "purple", player_pos, 40)
    pygame.draw.circle(screen, "red", player_pos_2, 40)
    pygame.draw.circle(screen, "green", player_pos_3, 40)

    keys = pygame.key.get_pressed()

    # print(f"{}")
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
        if player_pos.y > 720:
            player_pos.y -= 720
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
        if player_pos.y > 720:
            player_pos.y -= 720
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
        if player_pos.x > 1280:
            player_pos.x -= 1280
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        if player_pos.x > 1280:
            player_pos.x -= 1280
    if keys[pygame.K_w]:
        player_pos_2.y -= 300 * dt
        if player_pos.y > 720:
            player_pos.y -= 720
    if keys[pygame.K_s]:
        player_pos_2.y += 300 * dt
        if player_pos.y > 720:
            player_pos.y -= 720
    if keys[pygame.K_a]:
        player_pos_2.x -= 300 * dt
        if player_pos.x > 1280:
            player_pos.x -= 1280
    if keys[pygame.K_d]:
        player_pos_2.x += 300 * dt
        if player_pos.x > 1280:
            player_pos.x -= 1280
    if keys[pygame.K_i]:
        player_pos_3.y -= 300 * dt
        if player_pos_3.y > 720:
            player_pos_3.y -= 720
    if keys[pygame.K_k]:
        player_pos_3.y += 300 * dt
        if player_pos_3.y > 720:
            player_pos_3.y -= 720
    if keys[pygame.K_j]:
        player_pos_3.x -= 300 * dt
        if player_pos_3.x > 1280:
            player_pos_3.x -= 1280
    if keys[pygame.K_l]:
        player_pos_3.x += 300 * dt
        if player_pos_3.x > 1280:
            player_pos_3.x -= 1280
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
