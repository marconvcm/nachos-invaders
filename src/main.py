#   \ |    \     __|  |  |   _ \   _ _|   \ | \ \   /  \    _ \  __|  _ \   __| 
#  .  |   _ \   (     __ |  (   |    |   .  |  \ \ /  _ \   |  | _|     / \__ \ 
# _|\_| _/  _\ \___| _| _| \___/   ___| _|\_|   \_/ _/  _\ ___/ ___| _|_\ ____/ 

import asyncio
import pygame
import os

from engine.scene import Menu, GameOver, SceneController
from engine.game import Game

# Initialize pygame


def aliens_groups_file():
   with open(os.path.abspath("aliens_groups.txt"), "r") as file:
      return file.read().split("-----")
   
def spritesheet(width, height):
   sheet = pygame.image.load(os.path.abspath("img/spritesheet.png")).convert()
   sheet_rect = sheet.get_rect()
   sprites = {}
   
   for y in range(sheet_rect.h // height):
      for x in range(sheet_rect.w // width):
         frame_location = (x * width, y * height, width, height)
         sprites["{}x{}".format(x, y)] = sheet.subsurface(frame_location)
   
   return sprites

async def main():

   pygame.init()
   pygame.font.init()

   global IS_RUNNING, DELTA, SCREEN, CLOCK, SIZE, WIDTH, HEIGHT

   SIZE = WIDTH, HEIGHT = 800, 600

   BLANK_COLOR = (55, 55, 55)
   SCREEN = pygame.display.set_mode(SIZE)
   CLOCK = pygame.time.Clock()
   IS_RUNNING = True
   DELTA = 0
   
   aliens_groups = aliens_groups_file()

   game_scene = Game(SCREEN, aliens_groups, spritesheet(32, 32))
   menu_scene = Menu(SCREEN)
   game_over_scene = GameOver(SCREEN)

   scene_controller = SceneController([menu_scene, game_scene, game_over_scene])
   scene_controller.change_scene("menu")

   while IS_RUNNING:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            IS_RUNNING = False

      SCREEN.fill(BLANK_COLOR)

      scene_controller.loop(DELTA)
      
      pygame.display.flip()

      DELTA = CLOCK.tick(60) / 1000
      await asyncio.sleep(0)  # Very important, and keep it 0

   pygame.quit()

asyncio.run(main())