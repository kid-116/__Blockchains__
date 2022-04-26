from matplotlib.pyplot import text
import pygame
from sys import exit

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

TITLE = 'Runner'

FPS_CEIL = 60

# display vs regular surfaces (assets)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
# __ x
# |
# y
# (x, y)

clock = pygame.time.Clock()

# width = 100
# height = 200
# test_surface = pygame.Surface((width, height))
# test_surface.fill('Red')

# family, size
title_font = pygame.font.Font('font/pixeltype.ttf', 50)
# text, anti-aliasing color
text_surface = title_font.render('Runner', False, 'Black')

# convert is good practice
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

SNAIL_SPEED = 4
snail_surface = pygame.image.load('graphics/snail/snail_1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(bottomleft=(600, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(100, 300))

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # block image transfer
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))
    screen.blit(player_surface, player_rectangle)
    screen.blit(snail_surface, snail_rectangle)

    # collisions
    if player_rectangle.colliderect(snail_rectangle):
        print('collision')

    # update
    snail_rectangle.x -= SNAIL_SPEED
    if snail_rectangle.right < 0:
        snail_rectangle.left = WINDOW_WIDTH

    player_rectangle.left += 1

    pygame.display.update()
    clock.tick(FPS_CEIL) # 60fps is the ceil