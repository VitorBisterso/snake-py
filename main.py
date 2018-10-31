import pygame
from pygame.locals import *

from GameManager import GameManager

def initialize():
  game_manager = GameManager(20, 20, 32)
  game_loop(game_manager)

def game_loop(game_manager):
  # Game loop
  while not game_manager.should_quit:
    game_manager.update()
    game_manager.render()
    pygame.display.flip()


if __name__ == '__main__': initialize()