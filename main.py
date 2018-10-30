import pygame
from pygame.locals import *

from GameManager import GameManager

def initialize():
  game_manager = GameManager(20, 20, 32)
  game_loop(game_manager)

def game_loop(game_manager):
  # Game loop
  while 1:
    for event in pygame.event.get():
      if event.type == QUIT:
        return

    game_manager.render()
    pygame.display.flip()


if __name__ == '__main__': initialize()