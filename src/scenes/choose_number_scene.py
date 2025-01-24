import pygame
import math

from scenes.scene import Scene
from colors import *

from utils import map_value

import events

MIN_VALUE = 5
MAX_VALUE = 20

class ChooseNumberScene(Scene):
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, difficulty: str):
        
        # init fonts
        self.title_font = title_font
        self.text_font = text_font

        #init difficulty
        self.difficulty = difficulty

        # init titles
        if self.difficulty == "easy":
            self.difficulty_render = self.title_font.render("Mode facile", True, BLACK)
        elif self.difficulty == "medium":
            self.difficulty_render = self.title_font.render("Mode intermediaire", True, BLACK)
        elif self.difficulty == "hard":
            self.difficulty_render = self.title_font.render("Mode difficile", True, BLACK)

        self.title_render_1 = self.text_font.render("Choisissez le nombre de personnes", True, BLACK)
        self.title_render_2 = self.text_font.render("à faire traverser", True, BLACK)

        # init buttons
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        self.choose_order_button_render = self.text_font.render("Choisir l'ordre", True, BLACK)
        self.choose_order_button = pygame.Rect(0, 0, 200, 50)

        # init slider
        self.min_text_render = self.text_font.render(str(MIN_VALUE), True, BLACK)
        self.max_text_render = self.text_font.render(str(MAX_VALUE), True, BLACK)

        self.slider_cursor = pygame.Rect(0, 0, 20, 20)
        self.slider_cursor_grabbed = False

        self.current_number_value = MIN_VALUE
        self.current_number_render = self.text_font.render(f"Votre choix : {self.current_number_value}", True, BLACK)


        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")
            
            elif self.choose_order_button.collidepoint(event.pos):
                events.send_scene_change_event("choose_order_scene",
                                                difficulty=self.difficulty,
                                                nb_people=self.current_number_value)
            
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
            old_value = self.current_number_value

            if min_in_pixels <= mouse_x <= max_in_pixels:
                self.current_number_value = round(map_value(pygame.mouse.get_pos()[0], min_in_pixels, max_in_pixels, MIN_VALUE, MAX_VALUE))
            elif mouse_x < min_in_pixels:
                self.current_number_value = MIN_VALUE
            elif mouse_x > max_in_pixels:
                self.current_number_value = MAX_VALUE

            if self.current_number_value != old_value:
                self.current_number_render = self.text_font.render(f"Votre choix : {self.current_number_value}", True, BLACK)

        self.slider_cursor.centerx = window_width // 2 - 150 + map_value(self.current_number_value, MIN_VALUE, MAX_VALUE, 0, 300)
        self.slider_cursor.centery = window_height // 2
    
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))

        window_width = draw_surface.get_width()
        window_height = draw_surface.get_height()

        draw_surface.blit(self.difficulty_render, self.difficulty_render.get_rect(centerx=window_width // 2, y = 15))

        draw_surface.blit(self.title_render_1, self.title_render_1.get_rect(centerx=window_width // 2, y = 70))
        draw_surface.blit(self.title_render_2, self.title_render_2.get_rect(centerx=window_width // 2, y = 100))

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
                center=(window_width // 2 - 200, window_height // 2)
            ))
        draw_surface.blit(self.max_text_render, self.max_text_render.get_rect(
                center=(window_width // 2 + 200, window_height // 2)
            ))
        
        draw_surface.blit(self.current_number_render, self.current_number_render.get_rect(
                center=(window_width // 2, window_height // 2 + 50)
            ))
        
        # next button
        self.choose_order_button.centerx = window_width // 2
        self.choose_order_button.centery = window_height - 100

        pygame.draw.rect(draw_surface, GREY, self.choose_order_button, border_radius=5)
        draw_surface.blit(self.choose_order_button_render, self.choose_order_button_render.get_rect(center=self.choose_order_button.center))



