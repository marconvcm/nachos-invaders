import pygame;

PLAYER_UP = 'up'
PLAYER_DOWN = 'down'
PLAYER_LEFT = 'left'
PLAYER_RIGHT = 'right'
PLAYER_ACTION_0 = 'action_0'
PLAYER_ACTION_1 = 'action_1'
PLAYER_ACTION_2 = 'action_2'
PLAYER_ACTION_3 = 'action_3'   

ACTION_MAP = {
   PLAYER_UP: [pygame.K_w, pygame.K_UP],
   PLAYER_DOWN: [pygame.K_s, pygame.K_DOWN],
   PLAYER_LEFT: [pygame.K_a, pygame.K_LEFT],
   PLAYER_RIGHT: [pygame.K_d, pygame.K_RIGHT],
   PLAYER_ACTION_0: [pygame.K_h, pygame.K_z],
   PLAYER_ACTION_1: [pygame.K_j, pygame.K_x],
   PLAYER_ACTION_2: [pygame.K_k, pygame.K_c],
   PLAYER_ACTION_3: [pygame.K_l, pygame.K_v]
}

class InputManager:
   def __init__(self):
      self.keys = pygame.key.get_pressed()

   def update(self):
      self.keys = pygame.key.get_pressed()

   def get_key(self, key):
      return self.keys[ACTION_MAP[key][0]] or self.keys[ACTION_MAP[key][1]]
   
   def is_action_pressed(self, action):
      return self.get_key(action)
