import pygame

from scenes.scene import Scene

class ChooseNumberScene(Scene):
    def __init__(self, title_font: pygame.Font):
        
        self.title_font = title_font
        self.current_number_value = 5

        self.title_render = self.title_font.render("Nombre de personnes", True, (255, 255, 255))

        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        ...
    
    def update(self, dt: float, *args: list, **kwargs: dict):
        ...
    
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((0, 255, 0))

        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(draw_surface.get_width() / 2, 30)))


