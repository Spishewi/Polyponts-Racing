from scenes.scene import Scene

import pygame

#define the colors
black = (0, 0, 0) 
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

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
        self.title_render = title_font.render("Bienvenue dans le jeu!", True, black )
        self.button_font = button_font
        #init of buttons
        self.BORDER_RADIUS_BUTTON = 5
        window_width = pygame.display.get_surface().get_width()
        self.button_easy_render = button_font.render("Mode facile", True, black)
        self.button_easy = pygame.Rect(window_width//2-width_button//2, y_button, width_button, height_button)  # Position (x, y), width, height
        self.button_medium_render = button_font.render("Mode intermediaire", True, black)
        self.button_medium = pygame.Rect(window_width//2-width_button//2, y_button+height_button+dt_space, width_button, height_button)
        self.button_hard_render = button_font.render("Mode difficile", True, black)
        self.button_hard = pygame.Rect(window_width//2-width_button//2, y_button+(height_button+dt_space)*2, width_button, height_button)
        #init of image 
        self.settings = 
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict) -> None:
        ...
    def update(self, dt: float, *args: list, **kwargs: dict) -> None:
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict) -> None:
        draw_surface.fill("white")
        
        #draw main title
        title_width = draw_surface.get_width() //2
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(title_width, 30)))
        

        #draw button easy
        pygame.draw.rect(draw_surface, green, self.button_easy, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_easy = self.button_easy_render.get_rect(center=self.button_easy.center)
        #Display the text on the button easy 
        draw_surface.blit(self.button_easy_render, text_button_easy)

        #draw button medium
        pygame.draw.rect(draw_surface, orange, self.button_medium, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_medium = self.button_medium_render.get_rect(center=self.button_medium.center)
        #Display the text on the button medium 
        draw_surface.blit(self.button_medium_render, text_button_medium)

        #draw button hard
        pygame.draw.rect(draw_surface, red, self.button_hard, border_radius=self.BORDER_RADIUS_BUTTON)
        text_button_hard = self.button_hard_render.get_rect(center=self.button_hard.center)
        #Display the text on the button easy 
        draw_surface.blit(self.button_hard_render, text_button_hard)

        ...
