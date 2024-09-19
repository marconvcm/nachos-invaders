import pygame;
from pygame.math import clamp;

DEFAULT_LOADING_TIME = 0.5

class Scene():
   def __init__(self, screen, payload = {}):
      super().__init__()
      self.payload = {}
      self.is_active = False
      self.screen = screen
      self.name = "[scene_name]"
      self.scene_controller = None
      self.loading = 0

   def loop(self, delta):
       self.loading = clamp(self.loading + delta, 0, DEFAULT_LOADING_TIME)
       pass
   
   def on_start(self):
      self.loading = 0
      pass

   def on_finish(self):
      self.loading = 0
      pass

   def is_loaded(self):
       return self.loading >= DEFAULT_LOADING_TIME

class BaseUIScene(Scene):
   def __init__(self, screen, name, next_scene, payload = {}):
      super().__init__(screen, payload)
      self.is_active = False
      self.name = name
      self.next_scene = next_scene
      self.font = pygame.font.Font(None, 24)
      self.current_line = 0
      self.lines = []
      self.line_height = 1
   
   def loop(self, delta):
      super().loop(delta)
      for line, rect in self.lines:
         self.screen.blit(line, rect)
      if self.is_loaded() and pygame.key.get_pressed()[pygame.K_SPACE]:
         self.scene_controller.change_scene(self.next_scene)

   def add_line(self, text):
      cen_x, cen_y = self.screen.get_rect().center
      line = self.font.render(text, True, (255, 255, 255))
      rect = line.get_rect(center=(cen_x, cen_y + (self.current_line * (self.line_height * 24))))
      self.lines.append((line, rect))
      self.current_line += 1

class Menu(BaseUIScene):
   def __init__(self, screen):
      super().__init__(screen, name = "menu", next_scene = "game", payload = {})
      
      
   def on_start(self):
      self.current_line = 0
      self.lines = []
      self.add_line("Nachos Invaders")
      
      if "level" in self.payload:
         current_level = self.payload["level"]
         self.add_line(f"Level: {current_level}")

      if not "level" in self.payload:
         self.add_line("")
         self.add_line("-------------------------")
         self.add_line("Instructions:")
         self.add_line("Use LEFT (A) and RIGHT (D) arrows to move")
         self.add_line("Use Z (H) to shoot")
         self.add_line("-------------------------")
         self.add_line("")
         self.add_line("Your objective is to destroy all aliens")
      
      self.add_line("Press SPACE to start")

class GameOver(BaseUIScene):
   def __init__(self, screen):
      super().__init__(screen, name = "game_over", next_scene = "menu", payload = {})

   def on_start(self):
      self.current_line = 0
      self.lines = []
      self.add_line("Game Over")
      self.add_line(f"Score: {self.payload['score']}")
      self.add_line("Press SPACE to return to menu")

class SceneController():
   def __init__(self, scenes):
      self.scenes = scenes
      self.current_scene = None
      for scene in self.scenes:
         scene.scene_controller = self

   def loop(self, delta):
      self.current_scene.loop(delta)

   def change_scene(self, scene_name, payload = {}):
      for scene in self.scenes:
         if scene.name == scene_name:
            self.disable_current_scene()
            self.current_scene = scene
            self.current_scene.payload = payload
            self.enable_current_scene()
            break
   
   def disable_current_scene(self):
      if self.current_scene is None:
         return
      self.current_scene.is_active = False
      self.current_scene.on_finish()
   
   def enable_current_scene(self):
      self.current_scene.is_active = True
      self.current_scene.on_start()