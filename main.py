import pygame
from pygame.locals import *

from GameManager import GameManager

def initialize():
  game_menu()

def game_menu():
  game_manager = GameManager(20, 20, 32)
  #while game_manager.menu:
    #pass
  game_loop(game_manager)

def game_loop(game_manager):
  # Game loop
  while not game_manager.should_quit and not game_manager.menu:
    game_manager.update()
    game_manager.render()
    pygame.display.flip()


if __name__ == '__main__': initialize()