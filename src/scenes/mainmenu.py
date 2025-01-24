from scenes.scene import Scene

import pygame

from colors import *
import events


#button dimension and position
height_button = 80 #hauteur
width_button = 300 #largeur
y_button = 100
dt_space = 20

class MainMenu(Scene):
    ...
    def __init__(self, title_font:pygame.Font , button_font:pygame.Font):
        #init of fronts for buttons and title
        self.title_font = title_font
        self.title_render = title_font.render("Bienvenue dans le jeu!", True, BLACK )
        self.button_font = button_font
        #init of buttons
        self.BORDER_RADIUS_BUTTON = 5
        window_width = pygame.display.get_surface().get_width()
        window_height = pygame.display.get_surface().get_height()
        self.button_easy_render = button_font.render("Mode facile", True, BLACK)
        self.button_easy = pygame.Rect(window_width//2-width_button//2, y_button, width_button, height_button)  # Position (x, y), width, height
        self.button_medium_render = button_font.render("Mode intermediaire", True, BLACK)
        self.button_medium = pygame.Rect(window_width//2-width_button//2, y_button+height_button+dt_space, width_button, height_button)
        self.button_hard_render = button_font.render("Mode difficile", True, BLACK)
        self.button_hard = pygame.Rect(window_width//2-width_button//2, y_button+(height_button+dt_space)*2, width_button, height_button)
        #init of image 
        self.settings = pygame.image.load('./assets/icons/settings.png') 
        self.tutorial = pygame.image.load('./assets/icons/help.png')

    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict) -> None:
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_easy.collidepoint(event.pos):
                events.send_scene_change_event("choose_number_scene", difficulty="easy")
            if self.button_medium.collidepoint(event.pos):
                events.send_scene_change_event("choose_number_scene", difficulty="medium")
            if self.button_hard.collidepoint(event.pos):
                events.send_scene_change_event("choose_number_scene", difficulty="hard")
        
        
    def update(self, dt: float, *args: list, **kwargs: dict) -> None:
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict) -> None:
        draw_surface.fill("white")
        #get window size 
        window_width = pygame.display.get_surface().get_width()
        window_height = pygame.display.get_surface().get_height()
        #draw main title
        title_width = draw_surface.get_width() //2
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(title_width, 30)))
        
        #draw button easy
        pygame.draw.rect(draw_surface, GREEN, self.button_easy, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_easy = self.button_easy_render.get_rect(center=self.button_easy.center)
        #Display the text on the button easy 
        draw_surface.blit(self.button_easy_render, text_button_easy)

        #draw button medium
        pygame.draw.rect(draw_surface, ORANGE, self.button_medium, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_medium = self.button_medium_render.get_rect(center=self.button_medium.center)
        #Display the text on the button medium 
        draw_surface.blit(self.button_medium_render, text_button_medium)

        #draw button hard
        pygame.draw.rect(draw_surface, RED, self.button_hard, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_hard = self.button_hard_render.get_rect(center=self.button_hard.center)
        #Display the text on the button easy 
        draw_surface.blit(self.button_hard_render, text_button_hard)

        #draw image
        draw_surface.blit(self.settings, self.settings.get_rect(center=(self.settings.get_width()+5,window_height-self.settings.get_height()+5)))
        draw_surface.blit(self.tutorial, self.tutorial.get_rect(center=(window_width-self.tutorial.get_width()+5, window_height-self.tutorial.get_width()+5)))
        ...
