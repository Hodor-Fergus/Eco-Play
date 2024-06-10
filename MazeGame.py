from game import game

import pygame

pygame.init()

screen = pygame.display.set_mode((1120, 800))
pygame.display.set_caption("ECO PLAY")
icon = pygame.image.load('./assets/icon/earth.png').convert_alpha()
pygame.display.set_icon(icon)

my_game = game((1120, 750), (1120/14, 800/10) , (40, 40), 1, 8, [9, 1])
my_game.run(screen)

pygame.quit()