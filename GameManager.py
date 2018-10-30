import pygame
import random
from pygame.locals import *

class GameManager:
  # Fruit variables
  fruit_x = 0
  fruit_y = 0

  # Snake variables
  snake_x = 0
  snake_y = 0
  direction = 0
  snake_size = 0
  
  def __init__(self, th, tv, ts):
    self.tiles_horizontally = th
    self.tiles_vertically = tv
    self.tiles_size = ts

    # Initialize screen
    pygame.init()
    self.screen = pygame.display.set_mode((self.tiles_horizontally * self.tiles_size, self.tiles_vertically * self.tiles_size))
    pygame.display.set_caption('Snake')
    icon = pygame.image.load("assets/imgs/snake.png")
    pygame.display.set_icon(icon)

    # Fill background
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))

    # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Snake", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = self.background.get_rect().centerx
    # self.background.blit(text, textpos)

    self.snake_x = random.uniform(0, self.tiles_horizontally * self.tiles_size)
    self.snake_y = random.uniform(0, self.tiles_vertically * self.tiles_size)

    self.fruit_x = random.uniform(0, self.tiles_horizontally * self.tiles_size)
    self.fruit_y = random.uniform(0, self.tiles_vertically * self.tiles_size)

    self.snake_image = pygame.image.load("assets/imgs/snake.bmp").convert()
    self.fruit_image = pygame.image.load("assets/imgs/fruit.bmp").convert()

    self.screen.blit(self.snake_image, (self.snake_x, self.snake_y))
    self.screen.blit(self.fruit_image, (self.fruit_x, self.fruit_y))
  
  def render(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.snake_image, (self.snake_x, self.snake_y))
    self.screen.blit(self.fruit_image, (self.fruit_x, self.fruit_y))
  
  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        return