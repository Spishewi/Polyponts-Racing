from scenes.scene import Scene
import pygame
from colors import *
import events
from utils import multiple_render
class TutorialScene(Scene):
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
    
        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init render
        self.title_render = self.title_font.render("Tutorial", True, BLACK)

        #init button
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        #init text
        text = "Le but de ce jeu est d'illustrer le problème d'agencement à deux machines. Pour cela, tu dois choisir un nombre de personnes entre 5 et 20, chacune ayant un temps de traversée spécifique sur deux ponts. Il est important de noter qu'il ne peut y avoir plus d'une personne sur la plateforme reliant les deux ponts à la fois. Ton objectif est de planifier l'ordre de passage des personnes de manière à optimiser leur traversée, le but étant de faire passer les personnes en moins de temps possible"
        self.text_render = multiple_render(text, text_font)

    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")

    def update(self, dt: float, *args: list, **kwargs: dict):
        ...

    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill(BACKGROUND_COLOR)
        #get window size 
        window_width = pygame.display.get_surface().get_width()
        
        #draw main title
        middle_width = draw_surface.get_width() //2
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(middle_width, 30)))
        
        #draw button back
        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))
        
        #draw text
        TutorialScene.draw_text(self, draw_surface, window_width)
        
    
    def draw_text(self, draw_surface:pygame.Surface, window_width: int):
        #constant
        x_offset = 30  
        y_offset = 90  
        x_gap = 10 
        y_gap = 40
        
        #variable
        number_line = 0
        max_line_width = window_width - 40  
        line_width = 0  
        number_line = 0

        for word in self.text_render:
            # Get the width of the current word
            word_width = word.get_width()
            # Check if the word can fit on the current line
            if word_width + line_width <= max_line_width:
                draw_surface.blit(word, (x_offset + line_width, y_offset + y_gap * number_line))
                line_width += word_width + x_gap
            else:
                # If the word doesn't fit, move to the next line
                number_line += 1
                line_width = word_width + x_gap
                draw_surface.blit(word, (x_offset, y_offset + number_line * y_gap))