import pygame

DEFAULT_MOVE_RATE = 2
ALIEN_SIZE = 24

class Alien(pygame.sprite.Sprite):

   def __init__(self, pos, move_scale = 1, movement_loop = "DLDR", sprite=None):
      super().__init__()
      if sprite is None:
         self.image = pygame.Surface((ALIEN_SIZE, ALIEN_SIZE))
         self.image.fill("green")
      else:
         self.image = sprite
      
      self.rect = self.image.get_rect(center=pos)
      self.speed = ALIEN_SIZE / 2
      self.move_scale = move_scale
      self.move_rate = DEFAULT_MOVE_RATE * self.move_scale
      self.is_alive = True
      self.movement_loop = movement_loop
      self.move_index = 0

   def update(self, delta):
      
      if self.move_rate <= 0:
         self.move()
         self.move_index = (self.move_index + 1) % len(self.movement_loop)
         self.move_rate = DEFAULT_MOVE_RATE * self.move_scale
      
      self.move_rate -= delta

      if self.rect.bottom > 600:
         self.is_alive = False

      if not self.is_alive:
         self.kill()

   def move(self):
      if self.movement_loop[self.move_index] == "R":
         self.rect.x += self.speed * 2
      elif self.movement_loop[self.move_index] == "L":
         self.rect.x -= self.speed * 2
      elif self.movement_loop[self.move_index] == "U":
         self.rect.y -= self.speed
      elif self.movement_loop[self.move_index] == "D":
         self.rect.y += self.speed

   def draw(self, screen):
      screen.blit(self.image, self.rect)

   def check_hit(self, shoots):
      for shoot in shoots:
         if self.rect.colliderect(shoot.rect):
            return shoot.hit(self)


def spawn_aliens(initial_pos=(800 / 2, 64), alien_grid=(10, 5), alien_gap = (48, 32), move_scale = 1):
   
   initial_x, initial_y = initial_pos
   gap_x, gap_y = alien_gap
   aliens = pygame.sprite.Group()

   for y in range(alien_grid[1]):
      for x in range(alien_grid[0]):
         pos_x = (x - alien_grid[0] / 2) * gap_x + initial_x
         pos_y = y * gap_y + initial_y
         aliens.add(Alien((pos_x, pos_y), move_scale))

   return aliens

# Alien Groupe Example
#
# 11111
# 01110
# 10101
#
# Where 1 is an alien and 0 is an empty space
def spawn_group(alien_group, initial_pos=(800 / 2, 64), alien_gap = (48, 32), move_scale = 1, sprite=None):
   
   aliens = pygame.sprite.Group()   
   initial_x, initial_y = initial_pos
   gap_x, gap_y = alien_gap

   for y, row in enumerate(alien_group.splitlines()):
      for x, col in enumerate(row):
         if col == "1":
            pos_x = (x - len(row) / 2) * gap_x + initial_x
            pos_y = y * gap_y + initial_y
            aliens.add(Alien((pos_x, pos_y), move_scale, sprite=sprite))

   return aliens
