import pygame
from pygame.math import clamp

DEFAULT_FONT_SIZE = 24

class UI():
   
   def __init__(self, screen, player, aliens, game_data):
      self.screen = screen
      self.font = pygame.font.Font(None, DEFAULT_FONT_SIZE)
      self.player = player
      self.aliens = aliens
      self.game_data = game_data
      self.life_bar = pygame.surface.Surface((100, 10))

   def update(self, delta):
      lives = self.game_data["lives"]
      self.life_bar = pygame.surface.Surface((clamp(lives * 10, 0, 30), 10))
      self.life_bar.fill((255, 0, 0))

   def draw(self):
      score_text = self.font.render(f"Score: {self.game_data['score']}", True, (255, 255, 255))
      y = 0
      self.screen.blit(self.life_bar, (DEFAULT_FONT_SIZE, DEFAULT_FONT_SIZE))
      y += 12 + DEFAULT_FONT_SIZE
      for text in [score_text]:
         y += 12 + DEFAULT_FONT_SIZE
         self.screen.blit(text, (DEFAULT_FONT_SIZE, y))
