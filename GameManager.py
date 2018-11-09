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

    # Carrega as imagens da fruta, da cobra e do plano de fundo do menu
    self.snake_image = pygame.image.load("assets/imgs/snake.bmp").convert()
    self.fruit_image = pygame.image.load("assets/imgs/fruit.bmp").convert()
    self.bg = pygame.image.load("assets/imgs/menu_bg.png")
  
    # Inicializa os textos
    font = pygame.font.Font(None, 36)
    self.restart_text = font.render("Press 'r' to restart", 1, (10, 10, 10))
    self.restart_text_pos = self.restart_text.get_rect()
    self.restart_text_pos.centerx = self.background.get_rect().centerx
    self.restart_text_pos.centery = self.background.get_rect().centery

    self.menu_text_title = font.render("Snake", 1, (10, 10, 10))
    self.menu_text_title_pos = self.menu_text_title.get_rect()
    self.menu_text_title_pos.centerx = self.background.get_rect().centerx
    self.menu_text_title_pos.centery = self.background.get_rect().centery - 200

    # Variavel auxiliar (indica se o menu deve ser mostrado)
    self.menu = True

    self.game_menu()

  def quitgame(self):
    pygame.quit()
    quit()
  
  def options(self):
    print('options')

  def build_button(self, x, y, width, height, label, action):
    # desenha o botao
    pygame.draw.rect(self.screen, (151, 156, 163), Rect(x, y, width, height))

    #desenha o texto do botao
    button_text_font = pygame.font.Font(None, 30)
    button_text = button_text_font.render(label, 1, (0, 0, 0))
    button_text_pos = button_text.get_rect()
    button_text_pos.center = (x+(width/2), y+(height/2))
    self.screen.blit(button_text, button_text_pos)

    
    mouse_pos = pygame.mouse.get_pos()

    # verifica se foi clicado com o botao esquerdo
    if pygame.mouse.get_pressed()[0] == 1:
      # verifica se a posicao do mouse esta dentro do botao
      if x+width > mouse_pos[0] > x and y+height > mouse_pos[1] > y:
        action()

  # Mostra o menu
  def game_menu(self):
    while self.menu:
      
      # Desenha o plano de fundo
      self.screen.blit(self.bg, (0, 0))

      # Desenha o titulo do jogo
      self.screen.blit(self.menu_text_title, self.menu_text_title_pos)

      # Constroi os botoes
      self.build_button(self.background.get_rect().centerx-125, self.background.get_rect().centery - 150, 250, 50, "Play", self.restart)
      self.build_button(self.background.get_rect().centerx-125, self.background.get_rect().centery - 50, 250, 50, "Options", self.options)
      self.build_button(self.background.get_rect().centerx-125, self.background.get_rect().centery + 50, 250, 50, "Quit", self.quitgame)

      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          quit()

      pygame.display.flip()

  # Randomiza a posição da fruta
  def random_fruit_position(self):
    while self.fruit_position in self.snake_position:
      self.fruit_position = (randint(0, self.tiles_horizontally - 1), randint(0, self.tiles_vertically - 1))

  # Reinicia todas as variáveis para recomeçar o jogo
  def restart(self):

    self.menu = False

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
    for snake_tile in self.snake_position:
      self.screen.blit(self.snake_image, (snake_tile[0] * self.tile_size, snake_tile[1] * self.tile_size))

    #Desenha a fruta
    self.screen.blit(self.fruit_image, (self.fruit_position[0] * self.tile_size, self.fruit_position[1] * self.tile_size))

    # Desenha a pontuação ou fim de jogo
    if (self.game_over):
      pygame.draw.rect(self.screen, (151, 156, 163), 
                       Rect(self.restart_text_pos.x - 10, 
                            self.restart_text_pos.y - 10, self.restart_text_pos.width + 20, self.restart_text_pos.height + 20))
      self.screen.blit(self.restart_text, self.restart_text_pos)

    self.screen.blit(self.display_text, self.display_text_pos)
  
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
          elif (event.key == pygame.K_ESCAPE):
            self.menu = True
            self.game_menu()
            break

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
            self.update_rate *= 0.98
            self.random_fruit_position()
          else:
            self.snake_position.pop(0)

        self.display_text_message = str(self.score)
    else:
      self.display_text_message = "Game over! Your score: " + str(self.score)
  
    font = pygame.font.Font(None, 36)
    self.display_text = font.render(self.display_text_message, 1, (10, 10, 10))
    self.display_text_pos = self.display_text.get_rect()
    self.display_text_pos.centerx = self.background.get_rect().centerx