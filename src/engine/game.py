import pygame

from engine.player import Player
from engine.input import InputManager
from engine.alien import spawn_group
from engine.ui import UI
from engine.scene import Scene

DEFAULT_LIVES = 3

class Game(Scene):
   def __init__(self, screen, aliens_groups, spritesheet):
      super().__init__(screen)

      self.difficulty = 1

      self.aliens_groups = aliens_groups
      self.spritesheet = spritesheet

      self.screen_w = self.screen.get_rect().w
      self.screen_h = self.screen.get_rect().h
      self.initial_pos = (self.screen_w // 2, self.screen_h - 64)

      self.is_active = False
      self.name = "game"
      
      self.input_manager = InputManager()

      self.player = Player(self.screen, self.initial_pos, self.input_manager, spritesheet["0x8"])
      self.aliens = pygame.sprite.Group()
      
      self.game_data = { "score": 0, "lives": 3, "current_level": -1 }
      self.ui = UI(self.screen, self.player, self.aliens, self.game_data)

   def loop(self, delta):
      if not self.is_active:
         return
      
      self.player.update(delta)
      self.player.draw(self.screen)

      for alien in self.aliens:
         alien.update(delta)
         alien.draw(self.screen)
         if alien.check_hit(self.player.shoots):
            self.game_data["score"] += 1

      for alien in self.aliens:
         if not alien.is_alive:
            self.aliens.remove(alien)

      for alien in self.aliens:
         if alien.rect.bottom > self.player.rect.top:
            self.game_data["lives"] -= 1
            self.aliens.remove(alien)

      
      self.ui.update(delta)
      self.ui.draw()

      if self.game_data["lives"] < 1:
         self.is_active = False
         self.reset_game()
         self.scene_controller.change_scene("game_over", payload=self.game_data)
         return;

      if len(self.aliens) == 0:
         self.is_active = False
         self.scene_controller.change_scene("menu", { "level": self.game_data["current_level"]+2 } )
   
   def on_start(self):
      self.difficulty += 1
      self.game_data["current_level"] = (self.game_data["current_level"] + 1) % len(self.aliens_groups)
      self.aliens = spawn_group(self.aliens_groups[self.game_data["current_level"]], alien_gap=(48, 48), move_scale = 1/(self.difficulty * 3), sprite=self.spritesheet["10x1"])
      self.player.reset()
   
   def reset_game(self):
      self.game_data["score"] = 0
      self.game_data["lives"] = DEFAULT_LIVES
      self.game_data["current_level"] = -1
      self.difficulty = 1
      self.aliens = pygame.sprite.Group()
      self.player.reset()