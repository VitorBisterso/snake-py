import pygame
from random import randint
from pygame.locals import *

class GameManager:
  # Constants
  UPDATE_RATE = 100

  # Game variables
  score = 0

  # Fruit variables
  fruit_position = (0, 0)

  # Snake variables
  snake_position = []
  snake_direction = 0
  snake_size = 0

  # Auxiliar variables
  should_quit = False
  last_tick = 0
  
  def __init__(self, th, tv, ts):
    self.tiles_horizontally = th
    self.tiles_vertically = tv
    self.tile_size = ts

    # Initialize screen
    pygame.init()
    self.screen = pygame.display.set_mode((self.tiles_horizontally * self.tile_size, self.tiles_vertically * self.tile_size))
    pygame.display.set_caption('Snake')
    icon = pygame.image.load("assets/imgs/snake.png")
    pygame.display.set_icon(icon)

    # Fill background
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))

    self.snake_position.insert(0,  (randint(0, self.tiles_horizontally), randint(0, self.tiles_vertically)))
    self.random_fruit_position()

    self.snake_image = pygame.image.load("assets/imgs/snake.bmp").convert()
    self.fruit_image = pygame.image.load("assets/imgs/fruit.bmp").convert()
  
  def random_fruit_position (self):
    self.fruit_position = (randint(0, self.tiles_horizontally), randint(0, self.tiles_vertically))

  def render(self):
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))
    self.screen.blit(self.background, (0, 0))

    for snake_tile in self.snake_position:
      self.screen.blit(self.snake_image, (snake_tile[0] * self.tile_size, snake_tile[1] * self.tile_size))

    self.screen.blit(self.fruit_image, (self.fruit_position[0] * self.tile_size, self.fruit_position[1] * self.tile_size))
  
    font = pygame.font.Font(None, 36)
    text = font.render(str(self.score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = self.background.get_rect().centerx
    self.background.blit(text, textpos)

  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.should_quit = True
        return

      elif event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_UP and (self.snake_direction != 2 or self.snake_size == 1)):
          self.snake_direction = 0
        elif (event.key == pygame.K_RIGHT and (self.snake_direction != 3 or self.snake_size == 1)):
          self.snake_direction = 1
        elif (event.key == pygame.K_DOWN and (self.snake_direction != 0 or self.snake_size == 1)):
          self.snake_direction = 2
        elif (event.key == pygame.K_LEFT and (self.snake_direction != 1 or self.snake_size == 1)):
          self.snake_direction = 3

    current_tick = pygame.time.get_ticks()
    if (current_tick - self.last_tick > self.UPDATE_RATE):
      self.last_tick = current_tick
      if self.snake_direction == 0:
        self.snake_position.insert(len(self.snake_position), (self.snake_position[-1][0], (self.snake_position[-1][1] - 1 + 20) % self.tiles_vertically))
      elif self.snake_direction == 1:
        self.snake_position.insert(len(self.snake_position), ((self.snake_position[-1][0] + 1) % self.tiles_horizontally, self.snake_position[-1][1]))
      elif self.snake_direction == 2:
        self.snake_position.insert(len(self.snake_position), (self.snake_position[-1][0], (self.snake_position[-1][1] + 1) % self.tiles_vertically))
      elif self.snake_direction == 3:
        self.snake_position.insert(len(self.snake_position), ((self.snake_position[-1][0] - 1 + 20) % self.tiles_horizontally, self.snake_position[-1][1]))
      
      if (self.snake_position[-1] == self.fruit_position):
        self.score += 1
        self.random_fruit_position()
      else:
        self.snake_position.pop(0)