# This file has been modified by Spishewi and Isteer from the exemple profided by pygbag

import asyncio
import pygame

#from scenes.mainmenu import MainMenu
from scenes.choose_number_scene import ChooseNumberScene

# Try to declare all your globals at once to facilitate compilation later.
RUNNING = True

LASTFRAME = 0

# Do init here
pygame.init()

screen = pygame.display.set_mode((640, 480), pygame.SCALED | pygame.RESIZABLE)

global_title_font = pygame.font.SysFont("comic sans ms", 32)

#mainmenu = MainMenu()
current_scene = ChooseNumberScene(global_title_font)




# Load any assets right now to avoid lag at runtime or network errors.


async def main():
    global RUNNING
    global LASTFRAME

    while RUNNING:
        # calculate delta time
        dt = (pygame.time.get_ticks() - LASTFRAME) / 1000
        dt = min(dt, 0.1)
        dt = max(dt, 0.00001)

        LASTFRAME = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            current_scene.event_handler(event)
            


        # Do your rendering here, note that it's NOT an infinite loop,
        # and it is fired only when VSYNC occurs
        # Usually 1/60 or more times per seconds on desktop
        # could be less on some mobile devices
        current_scene.update(dt)

        current_scene.draw(screen)

        pygame.display.update()
        await asyncio.sleep(0)  # Very important, and keep it 0

# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
