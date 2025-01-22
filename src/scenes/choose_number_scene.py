import pygame
import math

from scenes.scene import Scene
from colors import *

from utils import map_value

MIN_VALUE = 5
MAX_VALUE = 20

class ChooseNumberScene(Scene):
    def __init__(self, title_font: pygame.Font, button_font: pygame.Font):
        
        # init title
        self.title_font = title_font

        self.title_render = self.title_font.render("Nombre de personnes", True, BLACK)

        # init buttons
        self.button_font = button_font

        self.back_button_render = self.button_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        # init slider
        self.min_text_render = self.button_font.render(str(MIN_VALUE), True, BLACK)
        self.max_text_render = self.button_font.render(str(MAX_VALUE), True, BLACK)

        self.slider_cursor = pygame.Rect(0, 0, 20, 20)

        self.current_number_value = MIN_VALUE


        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                ... #send an event to go back
    
    def update(self, dt: float, *args: list, **kwargs: dict):    
        self.current_number_value = map_value(math.sin(pygame.time.get_ticks() / 1000), -1, 1, MIN_VALUE, MAX_VALUE)
    
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))

        window_width = draw_surface.get_width()
        window_height = draw_surface.get_height()

        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(window_width // 2, 30)))

        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))


        # oui c'est hardcodé, oui c'est pas beau. tkt.
        
        #center line
        pygame.draw.rect(draw_surface, BLACK, 
                         (window_width // 2 - 160, window_height // 2 - 3, 320, 6))
        
        # left line
        pygame.draw.rect(draw_surface, BLACK,
                         (window_width // 2 - 160 - 3, window_height // 2 - 10, 6, 20), border_radius=2)
        # right line
        pygame.draw.rect(draw_surface, BLACK,
                         (window_width // 2 + 160 - 3, window_height // 2 - 10, 6, 20), border_radius=2)
        
        # cursor
        self.slider_cursor.x = window_width // 2 - 160 + map_value(self.current_number_value, MIN_VALUE, MAX_VALUE, 0, 300)
        self.slider_cursor.y = window_height // 2 - 10
        
        pygame.draw.rect(draw_surface, GREY, self.slider_cursor, border_radius=2)
        
        draw_surface.blit(self.min_text_render, self.min_text_render.get_rect(
            center=(window_width // 2 - 200, window_height // 2)))
        draw_surface.blit(self.max_text_render, self.max_text_render.get_rect(
            center=(window_width // 2 + 200, window_height // 2)))


