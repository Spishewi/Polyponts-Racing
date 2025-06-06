import pygame
from scenes.scene import Scene
from colors import *
import events
import webbrowser

class ContributionScene(Scene):
    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init render
        self.title_render = title_font.render("Contributions", True, BLACK)
        self.text_render1 = text_font.render("Ce projet a été réalisé par", True, BLACK)
        self.text_render2 = text_font.render("Aurèle Aumont--Vesnier et Romain Blaquart.", True, BLACK)
        self.text_render3 = text_font.render("Sous la supervision de Jean-Charles Billaut.", True, BLACK)
        self.text_render4 = text_font.render("Crédits:", True, BLACK)
        self.text_render5 = text_font.render("- Police utilisée: m6x11. Réalisée par Daniel Linssen.", True, BLACK)
        self.text_render6 = text_font.render("- Dessin du personnage: Segel2D", True, BLACK)
        self.text_render7 = text_font.render("- Icônes: Lucide Contributors 2022", True, BLACK)
        self.flowshop_render = text_font.render("- Problème flow-shop à deux machines", True, BLACK)
        self.johnson_render = text_font.render("- Algorithme de Johnson 1954", True, BLACK)
        #init back button
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        #init link button
        self.link_button_render = self.text_font.render("Lien github", True, BLACK)
        self.link_button = pygame.Rect(20, 20, 250, 70)

        #github logo
        self.github = pygame.image.load('./assets/icons/github.png')
        ...

    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")
            elif self.link_button.collidepoint(event.pos):
                webbrowser.open("https://github.com/Spishewi/ProjetS4PEIP2")
                
    def update(self, dt: float, *args: list, **kwargs: dict):
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill(BACKGROUND_COLOR)
        window_width = draw_surface.get_width()
        window_height = draw_surface.get_height()
        y_offset = 35
        #draw back button
        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))
        
        #draw title
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(window_width // 2, y_offset)))

        #draw text
        y_start = 80
        y_gap = 40
        draw_surface.blit(self.text_render1, self.text_render1.get_rect(center=(window_width // 2, y_start)))
        draw_surface.blit(self.text_render2, self.text_render2.get_rect(center=(window_width // 2, y_start + y_gap)))
        draw_surface.blit(self.text_render3, self.text_render3.get_rect(center=(window_width // 2, y_start + 2 * y_gap)))
        draw_surface.blit(self.text_render4, self.text_render4.get_rect(center=(window_width // 2, y_start + 4 * y_gap)))
        draw_surface.blit(self.text_render5, self.text_render5.get_rect(center=(window_width // 2, y_start + 5 * y_gap)))
        draw_surface.blit(self.text_render6, self.text_render6.get_rect(center=(window_width // 2, y_start + 6 * y_gap)))
        draw_surface.blit(self.text_render7, self.text_render7.get_rect(center=(window_width // 2, y_start + 7 * y_gap)))
        draw_surface.blit(self.flowshop_render, self.flowshop_render.get_rect(center=(window_width // 2, y_start + 8*y_gap)))
        draw_surface.blit(self.johnson_render, self.johnson_render.get_rect(center=(window_width // 2, y_start + 9*y_gap)))
        
        #draw link button
        self.link_button.centerx = window_width // 2 
        self.link_button.centery = window_height - 90
        pygame.draw.rect(draw_surface, CARIBBEAN_CURRENT, self.link_button, border_radius=5)
        
        total_width = self.link_button_render.get_width() + self.github.get_width() + 10 
        text_x = self.link_button.centerx - total_width // 2
        image_x = text_x + self.link_button_render.get_width() + 10

        text_y = self.link_button.centery - self.link_button_render.get_height() // 2
        image_y = self.link_button.centery - self.github.get_height() // 2

        draw_surface.blit(self.link_button_render, (text_x, text_y))
        draw_surface.blit(self.github, (image_x, image_y))
   