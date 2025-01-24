from scenes.scene import Scene
import pygame 
from colors import *

class ChooseOrderScene(Scene):
    ...
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
        #init fot
        self.title_font = title_font
        self.text_font = text_font

        #init title
        self.title_render_1 = self.text_font.render("Choisissez l'ordre de passage", True, BLACK)
        self.title_render_2 = self.text_font.render("de vos personnages", True, BLACK)

        #init button play
        self.play_button_render = self.text_font.render("Play", True, BLACK)
        self.play_button = pygame.Rect(10, 10, 120, 70)
        #init button back
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)
    
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        ...
    
    def update(self, dt: float, *args: list, **kwargs: dict):
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))
        window_width = draw_surface.get_width()
        window_height = draw_surface.get_height()
        
        #draw title
        draw_surface.blit(self.title_render_1, self.title_render_1.get_rect(center=(window_width // 2, 30)))
        draw_surface.blit(self.title_render_2, self.title_render_2.get_rect(center=(window_width//2, 60)))
        #draw button back
        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))
        
        #draw button play
        pygame.draw.rect(draw_surface, ORANGE, self.play_button, border_radius=5)
        draw_surface.blit(self.play_button_render, self.play_button_render.get_rect(center=(window_width//2, window_height-5)))
        ...


    ...
    