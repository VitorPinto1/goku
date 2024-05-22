import pygame
from src.game import Game
import sys

pygame.init()
pygame.mixer.init() 
screen = pygame.display.set_mode((800, 600))

game = Game(screen)
game.run()
pygame.quit()