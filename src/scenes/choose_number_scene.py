import pygame
import math

from scenes.scene import Scene
from colors import *

from utils import map_value

import events

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
        self.slider_cursor_grabbed = False

        self.current_number_value = MIN_VALUE


        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")
            
            elif self.slider_cursor.collidepoint(event.pos):
                self.slider_cursor_grabbed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_cursor_grabbed = False

    def update(self, dt: float, *args: list, **kwargs: dict):
        window_width = pygame.display.get_surface().get_width()
        window_height = pygame.display.get_surface().get_height()

        #cursor
        if self.slider_cursor_grabbed:
            mouse_x = pygame.mouse.get_pos()[0]
            min_in_pixels = window_width // 2 - 150
            max_in_pixels = window_width // 2 + 150

            if min_in_pixels <= mouse_x <= max_in_pixels:
                self.current_number_value = map_value(pygame.mouse.get_pos()[0], min_in_pixels, max_in_pixels, MIN_VALUE, MAX_VALUE)
            elif mouse_x < min_in_pixels:
                self.current_number_value = MIN_VALUE
            elif mouse_x > max_in_pixels:
                self.current_number_value = MAX_VALUE

        self.slider_cursor.centerx = window_width // 2 - 150 + map_value(self.current_number_value, MIN_VALUE, MAX_VALUE, 0, 300)
        self.slider_cursor.centery = window_height // 2
    
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
        pygame.draw.rect(draw_surface, GREY, self.slider_cursor, border_radius=2)

        draw_surface.blit(self.min_text_render, self.min_text_render.get_rect(
            center=(window_width // 2 - 200, window_height // 2)))
        draw_surface.blit(self.max_text_render, self.max_text_render.get_rect(
            center=(window_width // 2 + 200, window_height // 2)))


