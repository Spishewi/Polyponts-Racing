from scenes.scene import Scene
import pygame
from colors import *
import events
from math import floor,pi
from utils import People, map_value, bridge_parabolla
from random import randint

class PlayScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, difficulty: str, people_list: list[People] ):
        #init difficulty and nb_people
        self.difficulty = difficulty
        self.people_list = people_list
        #window dimension
        window_height = pygame.display.get_surface().get_height()
        window_width = pygame.display.get_surface().get_width()
        dy = 130
        width_high = window_width//6
        width_low = window_width//8
        #init start platform
        self.start_platform_1 = pygame.Rect(0, dy, width_high, window_height/2-dy)
        self.start_platform_2 = pygame.Rect(0, window_height/2+dy+5, width_high, window_height/2-dy)

        #init mid platform
        self.mid_platform_1 = pygame.Rect(window_width/2-width_low, dy, width_low, window_height/2-dy)
        self.mid_platform_2 = pygame.Rect(window_width/2-width_low, window_height/2+dy+5, width_low, window_height/2-dy)

        #init finish plateform
        self.end_platform_1 = pygame.Rect(window_width-width_high, dy, width_high, window_height/2-dy)
        self.end_platform_2 = pygame.Rect(window_width-width_high, window_height/2+dy+5, width_high, window_height/2-dy )

        #init list people
        self.bridge1_list_people_ia = [People(i, randint(50, 150), randint(50, 150)) for i in range(len(self.people_list))]
        self.bridge2_people_ia = None
        self.bridge1_list_people_player = people_list
        self.bridge2_people_player = None

        self.bridge1_current_time_ia = 0
        self.bridge2_current_time_ia = 0
        self.bridge1_current_time_player = 0
        self.bridge2_current_time_player = 0

        #init people rect
        high_figure = 30
        self.people_player = pygame.Rect(self.start_platform_1.topright[0], self.start_platform_1.topright[1]-high_figure, 10, high_figure)
        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        ...
    def update(self, dt: float, *args: list, **kwargs: dict):

        # someone is walking on the player bridge 1
        if self.bridge1_current_time_player < self.bridge1_list_people_player[0].m1_time:
            self.bridge1_current_time_player += dt * 100

        # someone has finished walking on the bridge 1 and the bridge 2 is already used
        elif self.bridge2_people_player is not None:
            # wait for the people on bridge 2 to finish
            ...

        else:
            self.bridge2_people_player = self.bridge1_list_people_player.pop(0)
            self.bridge1_current_time_player = 0

        # someone is walking on the player bridge 1
        if self.bridge1_current_time_player < self.bridge1_list_people_player[0].m1_time:
            self.bridge1_current_time_player += dt * 100

        # someone has finished walking on the bridge 1 and the bridge 2 is already used
        elif self.bridge2_people_player is not None:
            # wait for the people on bridge 2 to finish
            ...

        else:
            self.bridge2_people_player = self.bridge1_list_people_player.pop(0)
            self.bridge1_current_time_player = 0
            

        
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255,255,255)) 
       
        #window dimension and useful things
        window_height = pygame.display.get_surface().get_height()
        window_width = pygame.display.get_surface().get_width()
        dy = 130
        width_high = window_width//6
        width_low = window_width//8

        #draw background water
        high_water = 250
        water_1 = pygame.Rect(0, high_water, window_width, window_height/2-high_water)
        pygame.draw.rect(draw_surface, BLUE, water_1)
        water_2 = pygame.Rect(0, window_height/2+high_water, window_width, window_height/2-high_water)
        pygame.draw.rect(draw_surface, BLUE, water_2)

        #draw start platform
        pygame.draw.rect(draw_surface, GREY, self.start_platform_1)
        pygame.draw.rect(draw_surface, GREY, self.start_platform_2)

        #draw line
        line_middle = pygame.Rect(0, window_height/2, window_width, 5)
        pygame.draw.rect(draw_surface, BLACK, line_middle)

        #draw middle plateform
        pygame.draw.rect(draw_surface, GREY, self.mid_platform_1)
        pygame.draw.rect(draw_surface, GREY, self.mid_platform_2) 

        #draw end plateform
        pygame.draw.rect(draw_surface, GREY, self.end_platform_1)
        pygame.draw.rect(draw_surface, GREY, self.end_platform_2)

        #draw bridge
        self._draw_bridge(draw_surface, self.start_platform_1, self.mid_platform_1)
        self._draw_bridge(draw_surface, self.start_platform_1, self.mid_platform_1)
        self._draw_bridge(draw_surface, self.mid_platform_1, self.end_platform_1)
        self._draw_bridge(draw_surface, self.start_platform_2, self.mid_platform_2)
        self._draw_bridge(draw_surface, self.mid_platform_2, self.end_platform_2)

        #draw People
        self.people_player.x = map_value(self.current_time_1, 0, self.list_player[0].m1_time, self.start_platform_1.topright[0], self.mid_platform_1.topleft[0])
        pygame.draw.rect(draw_surface, BLUE, self.people_player)
    
    def _draw_bridge(self, draw_surface: pygame.Surface, start_plateform: pygame.Rect, end_plateform: pygame.Rect):
        #set const
        circle_radius = 5
        step = 8
        height = 0.1
        
        scale = end_plateform.left - start_plateform.right
        
        for i in range(int(start_plateform.right) + step // 2, int(end_plateform.left), step):
            y = start_plateform.top + circle_radius // 2 + bridge_parabolla(height, map_value(i, start_plateform.right, end_plateform.left, 0, 1)) * scale
            pygame.draw.circle(draw_surface, BROWN, (i, y), circle_radius)
            
    def _draw_people(self, people_player, draw_surface: pygame.Surface, start_plateform: pygame.Rect):
        #set const
        ...
