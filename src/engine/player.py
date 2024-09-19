import pygame
from engine.input import PLAYER_DOWN, PLAYER_UP, PLAYER_LEFT, PLAYER_RIGHT, PLAYER_ACTION_0, InputManager

PLAYER_SIZE = 32
MAX_SHOOTS = 5
DEFAULT_FIRE_RATE = 0.1

class Player(pygame.sprite.Sprite):
   
   def __init__(self, screen, pos, input_manager, sprite):
      super().__init__()
      self.shoots = []
      self.initial_pos = pos
      self.input_manager = input_manager
      self.image = sprite
      self.bounds = screen.get_rect()
      self.rect = self.image.get_rect(center=screen.get_rect().center)
      self.rect.center = pos
      self.fire_rate = DEFAULT_FIRE_RATE
      self.speed = 300
      self.screen = screen

   def update(self, delta):
      self.input_manager.update()
      if self.input_manager.is_action_pressed(PLAYER_RIGHT):
         self.rect.x += self.speed * delta
      
      if self.input_manager.is_action_pressed(PLAYER_LEFT):
         self.rect.x -= self.speed * delta

      if self.rect.right > self.bounds.right:
         self.rect.right = self.bounds.right
      
      if self.rect.left < self.bounds.left:
         self.rect.left = self.bounds.left

      if self.input_manager.is_action_pressed(PLAYER_ACTION_0):
         if len(self.shoots) < MAX_SHOOTS and self.fire_rate <= 0:
            self.shoots.append(Shoot(self.rect.center))
            self.fire_rate = DEFAULT_FIRE_RATE
      
      self.fire_rate -= delta
      
      for shoot in self.shoots:
         shoot.update(delta)

      self.shoots = [shoot for shoot in self.shoots if shoot.is_alive]

   def remaing_shoots(self):
      return abs(MAX_SHOOTS - len(self.shoots))

   def draw(self, screen):
      screen.blit(self.image, self.rect)
      for shoot in self.shoots:
         shoot.draw(screen)

   def reset(self):
      self.shoots = []
      self.rect = self.image.get_rect(center=self.screen.get_rect().center)
      self.rect.center = self.initial_pos


class Shoot(pygame.sprite.Sprite):
   def __init__(self, pos):
      super().__init__()
      self.image = pygame.Surface((8, 8))
      self.image.fill("white")
      self.initial_pos = pos
      self.rect = self.image.get_rect(center=pos)
      self.speed = 500
      self.is_alive = True

   def update(self, delta):
      self.rect.y -= self.speed * delta
      if (self.rect.centery < -10):
         self.is_alive = False
         self.kill()

   def draw(self, screen):
      screen.blit(self.image, self.rect)

   def hit(self, alien):
      self.is_alive = False
      self.kill()
      alien.is_alive = False
      alien.kill()
      return True