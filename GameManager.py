import pygame
import math
from random import randint
from pygame import font
from pygame.locals import *

class GameManager:  
  def __init__(self, th, tv, ts):
    # Inicializa as variáveis para o tamanho da tela
    self.tiles_horizontally = th
    self.tiles_vertically = tv
    self.tile_size = ts

    # Inicializa a tela em si
    pygame.init()
    self.screen = pygame.display.set_mode((self.tiles_horizontally * self.tile_size, self.tiles_vertically * self.tile_size))
    pygame.display.set_caption('Snake')
    icon = pygame.image.load("assets/imgs/snake.png")
    pygame.display.set_icon(icon)

    # Preenche o fundo
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))

    # Carrega as imagens da fruta e da cobra
    self.snake_image = pygame.image.load("assets/imgs/snake.bmp").convert()
    self.fruit_image = pygame.image.load("assets/imgs/fruit.bmp").convert()
  
    self.restart()

  # Randomiza a posição da fruta
  def random_fruit_position(self):
    while self.fruit_position in self.snake_position:
      self.fruit_position = (randint(0, self.tiles_horizontally - 1), randint(0, self.tiles_vertically - 1))

  # Reinicia todas as variáveis para recomeçar o jogo
  def restart(self):
    # Variáveis de jogo
    self.score = 1
    self.game_over = False
    self.update_rate = 100

    # Variáveis da fruta
    self.fruit_position = (0, 0)

    # Variáveis da cobra
    self.snake_position = []
    self.snake_direction = 0
    self.snake_size = 1
    self.can_move = True

    # Variáveis auxiliares
    self.should_quit = False
    self.last_tick = 0

    # Randomiza a posição da cobra e da fruta
    self.snake_position.insert(0,  (randint(0, self.tiles_horizontally), randint(0, self.tiles_vertically)))
    self.fruit_position = (randint(0, self.tiles_horizontally - 1), randint(0, self.tiles_vertically - 1))

  # Desenha a tela
  def render(self):
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))
    self.screen.blit(self.background, (0, 0))

    # Desenha a cobra
    display_text = str(self.score)
    for snake_tile in self.snake_position:
      self.screen.blit(self.snake_image, (snake_tile[0] * self.tile_size, snake_tile[1] * self.tile_size))

    #Desenha a fruta
    self.screen.blit(self.fruit_image, (self.fruit_position[0] * self.tile_size, self.fruit_position[1] * self.tile_size))

    # Desenha a pontuação ou fim de jogo
    if (self.game_over):
      display_text = "Game Over! Your score: " + str(self.score)
      
      font = pygame.font.Font(None, 36)
      text = font.render("Press 'r' to restart", 1, (10, 10, 10))
      textpos = text.get_rect()
      textpos.centerx = self.background.get_rect().centerx
      textpos.centery = self.background.get_rect().centery
      pygame.draw.rect(self.screen, (151, 156, 163), 
                       Rect(textpos.x - 10, 
                            textpos.y - 10, textpos.width + 20, textpos.height + 20))
      self.screen.blit(text, textpos)

    font = pygame.font.Font(None, 36)
    text = font.render(display_text, 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = self.background.get_rect().centerx
    self.screen.blit(text, textpos)
  
  # Trata dos eventos
  def update(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.should_quit = True
        return

      # Trata eventos de teclado
      elif event.type == pygame.KEYDOWN:
        if (self.can_move):
          if (event.key == pygame.K_UP and (self.snake_direction != 2 or self.snake_size == 1)):
            self.snake_direction = 0
          elif (event.key == pygame.K_RIGHT and (self.snake_direction != 3 or self.snake_size == 1)):
            self.snake_direction = 1
          elif (event.key == pygame.K_DOWN and (self.snake_direction != 0 or self.snake_size == 1)):
            self.snake_direction = 2
          elif (event.key == pygame.K_LEFT and (self.snake_direction != 1 or self.snake_size == 1)):
            self.snake_direction = 3

          self.can_move = False
        elif (event.key == pygame.K_r and self.game_over):
          self.restart()

    # Trata a nova posição da cobra
    if (not self.game_over):
      next_position = (0, 0)
      current_tick = pygame.time.get_ticks()
      if (current_tick - self.last_tick > self.update_rate):
        self.last_tick = current_tick
        self.can_move = True
        if self.snake_direction == 0:
          next_position = (self.snake_position[-1][0], (self.snake_position[-1][1] - 1 + 20) % self.tiles_vertically)
        elif self.snake_direction == 1:
          next_position = ((self.snake_position[-1][0] + 1) % self.tiles_horizontally, self.snake_position[-1][1])
        elif self.snake_direction == 2:
          next_position = (self.snake_position[-1][0], (self.snake_position[-1][1] + 1) % self.tiles_vertically)
        elif self.snake_direction == 3:
          next_position = ((self.snake_position[-1][0] - 1 + 20) % self.tiles_horizontally, self.snake_position[-1][1])
        
        # Se a próxima posição é parte da cobra, o jogador perdeu
        if (next_position in self.snake_position):
          self.game_over = True
        else:
          # Avança a cobra
          self.snake_position.insert(len(self.snake_position), next_position)  
          if (next_position == self.fruit_position):
            self.score += 1
            self.snake_size += 1
            self.update_rate = math.log(self.update_rate, 1.09)
            self.random_fruit_position()
          else:
            self.snake_position.pop(0) 