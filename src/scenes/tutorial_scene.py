from scenes.scene import Scene
import pygame
import color *


class TutorialScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init render
        self.title_render = title_font.render("Tutorial", True, BLACK)

        #init button
        self.button_back_render = title_font.render("Retour", True, BLACK)
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        ...

    def update(self, dt: float, *args: list, **kwargs: dict):
        ...

    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))
        
        ...