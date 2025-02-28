from scenes.scene import Scene
import pygame
from colors import *
import events

class FinishScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
        window_width = pygame.display.get_surface().get_width()
        window_height = pygame.display.get_surface().get_height()

        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init title
        self.title_render = title_font.render("Résultat", True, BLACK)

        #init button finish
        self.button_render = text_font.render("Rejouer", True, BLACK)
        self.finish_button = pygame.Rect(window_width//2-self.button_render.get_width()/2, window_height-120, window_width/6, window_width/10)
        

    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.finish_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")

        
    def update(self, dt: float, *args: list, **kwargs: dict):

        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))
        window_width = draw_surface.get_width()
        
        #draw title
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(window_width // 2, 30)))

        #draw button 
        pygame.draw.rect(draw_surface, ORANGE, self.finish_button, border_radius=5)
        draw_surface.blit(self.button_render, self.button_render.get_rect(center=self.finish_button.center))