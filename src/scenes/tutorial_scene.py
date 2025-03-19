from scenes.scene import Scene
import pygame
from colors import *
import events
from utils import multiple_render

TUTORIAL_TEXT = "Le but de ce jeu est d'illustrer un problème d'ordonnancement : le flow-shop à deux machine. Concrètement, vous allez devoir aider des personnages à traverser des ponts le plus rapidement possible, en les triant dans l'ordre de votre choix. Vos personnages affronterons d'autres personnages triées par une IA très perfectionnée. Mais attention ! les ponts sont fragiles, et seulement une seule personne peut monter sur un pont à la fois. De plus, chaque personne met un temps différent à traverser chaque pont ! Il vous faudra donc trier les personnes afin d'optimiser le temps de passage de chaque personnes, et ainsi, battre le tri de l'IA."
class TutorialScene(Scene):
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
    
        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init render
        self.title_render = self.title_font.render("Didacticiel", True, BLACK)

        #init button
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        #init text
        text = TUTORIAL_TEXT
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