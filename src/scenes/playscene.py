from scenes.scene import Scene
import pygame
import colors *
import events

class PlayScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, difficulty, nb_people):
        #init plateforme 
        