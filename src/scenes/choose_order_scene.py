from scenes.scene import Scene
import pygame 
from colors import *
import events

class ChooseOrderScene(Scene):
    ...
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, difficulty, nb_people):
        #init font
        self.title_font = title_font
        self.text_font = text_font
        #init difficulty and nb_people
        self.difficulty = difficulty
        self.nb_people = nb_people
        #init title
        self.title_render_1 = self.text_font.render("Choisissez l'ordre de passage", True, BLACK)
        self.title_render_2 = self.text_font.render("de vos personnages", True, BLACK)

        #init button play
        self.play_button_render = self.text_font.render("Play", True, BLACK)
        #init button back
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)
    
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("choose_number_scene",
                                               difficulty=self.difficulty, nb_people=self.nb_people)
            ...
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
        play_button = pygame.Rect(window_width//2-self.play_button_render.get_width(), window_height-120, 100, 70)
        pygame.draw.rect(draw_surface, ORANGE, play_button, border_radius=5)
        draw_surface.blit(self.play_button_render, self.play_button_render.get_rect(center=play_button.center))
        ...


    ...
    