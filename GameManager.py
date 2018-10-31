import pygame
import random
from pygame.locals import *

class GameManager:
  # Game variables
  score = 0

  # Fruit variables
  fruit_x = 0
  fruit_y = 0

  # Snake variables
  snake_x = 0
  snake_y = 0
  snake_direction = 0
  snake_size = 0

  # Auxiliar variables
  should_quit = False
  
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

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(str(self.score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = self.background.get_rect().centerx
    self.background.blit(text, textpos)

    self.snake_x = random.uniform(0, self.tiles_horizontally * self.tiles_size)
    self.snake_y = random.uniform(0, self.tiles_vertically * self.tiles_size)

    self.fruit_x = random.uniform(0, self.tiles_horizontally * self.tiles_size)
    self.fruit_y = random.uniform(0, self.tiles_vertically * self.tiles_size)

    self.snake_image = pygame.image.load("assets/imgs/snake.bmp").convert()
    self.fruit_image = pygame.image.load("assets/imgs/fruit.bmp").convert()

    self.screen.blit(self.snake_image, (self.snake_x, self.snake_y))
    self.screen.blit(self.fruit_image, (self.fruit_x, self.fruit_y))
  
  def render(self):
    font = pygame.font.Font(None, 36)
    text = font.render(str(self.score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = self.background.get_rect().centerx
    self.background.blit(text, textpos)

    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.snake_image, (self.snake_x, self.snake_y))
    self.screen.blit(self.fruit_image, (self.fruit_x, self.fruit_y))
  
  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.should_quit = True
        return

      elif event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_UP and (self.snake_direction != 2 or self.snake_size == 1)):
          self.snake_direction = 0
        elif (event.key == pygame.K_RIGHT  and (self.snake_direction != 3 or self.snake_size == 1)):
          self.snake_direction = 1
        elif (event.key == pygame.K_DOWN  and (self.snake_direction != 0 or self.snake_size == 1)):
          self.snake_direction = 2
        elif (event.key == pygame.K_LEFT and (self.snake_direction != 1 or self.snake_size == 1)):
          self.snake_direction = 3