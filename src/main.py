# This file has been modified by Spishewi and Isteer from the exemple profided by pygbag

import asyncio
import pygame
import sys

#from scenes.mainmenu import MainMenu
from scenes.choose_number_scene import ChooseNumberScene
from scenes.mainmenu import MainMenu
from scenes.choose_order_scene import ChooseOrderScene
from scenes.play_scene import PlayScene
from scenes.finish_scene import FinishScene
from scenes.tutorial_scene import TutorialScene
from scenes.contribution_scene import ContributionScene
from utils import People
import events
# Try to declare all your globals at once to facilitate compilation later.

if sys.platform == 'emscripten':
    PLATFORM = "wasm"
else:
    PLATFORM = "desktop"
RUNNING = True

LASTFRAME = 0
SPEED_FACTOR = 1

# Do init here
pygame.init()

TITLE_FONT_SIZE = 54
TEXT_FONT_SIZE = 36

pygame.display.set_caption("Polyponts Racing")
screen = pygame.display.set_mode((800, 600))

GLOBAL_TITLE_FONT = pygame.font.Font("./assets/fonts/m6x11plus.ttf", TITLE_FONT_SIZE)
GLOBAL_TEXT_FONT = pygame.font.Font("./assets/fonts/m6x11plus.ttf", TEXT_FONT_SIZE)

#current_scene = PlayScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, 4, [People(1,1,1)])
current_scene = FinishScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT)

clock = pygame.time.Clock()


# Load any assets right now to avoid lag at runtime or network errors.

async def main():
    global RUNNING
    global LASTFRAME
    global current_scene

    global SPEED_FACTOR


    while RUNNING:
        # calculate delta time
        if PLATFORM == "wasm":
            dt = (pygame.time.get_ticks() - LASTFRAME) / 1000
            LASTFRAME = pygame.time.get_ticks()
        else:
            dt = clock.tick(120) / 1000
        # prevent too big delta time (lagspikes)
        dt = min(dt, 0.5)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            elif event.type == events.SCENE_CHANGE:
                if event.scene == "mainmenu":
                    current_scene = MainMenu(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "choose_number_scene":
                    current_scene = ChooseNumberScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "choose_order_scene":
                    current_scene = ChooseOrderScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "play_scene":
                    current_scene = PlayScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "finish_scene":
                    current_scene = FinishScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "tutorial_scene":
                    current_scene = TutorialScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)
                elif event.scene == "contribution_scene":
                    current_scene = ContributionScene(GLOBAL_TITLE_FONT, GLOBAL_TEXT_FONT, **event.scene_args)            # Speed up the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SPEED_FACTOR = 10
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    SPEED_FACTOR = 1


            current_scene.event_handler(event)
            

        # comments from exemple file.
        # Do your rendering here, note that it's NOT an infinite loop,
        # and it is fired only when VSYNC occurs
        # Usually 1/60 or more times per seconds on desktop
        # could be less on some mobile devices
        current_scene.update(dt * SPEED_FACTOR)

        current_scene.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0)  # Very important, and keep it 0

# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
