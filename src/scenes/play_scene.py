from scenes.scene import Scene
import pygame
from colors import *
import events
from math import floor,pi
from utils import People, map_value
from random import randint

class PlayScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font):
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
        self.list_ia = [People(i, randint(50, 150), randint(50, 150)) for i in range(8)]
        self.list_player = [People(i, randint(50, 150), randint(50, 150)) for i in range(8)]
        self.current_time_1 = 0
        self.current_time_2 = 0

        #init people rect
        high_figure = 30
        self.people_player = pygame.Rect(self.start_platform_1.topright[0], self.start_platform_1.topright[1]-high_figure, 10, high_figure)
        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        ...
    def update(self, dt: float, *args: list, **kwargs: dict):
        time_1_player = self.list_player[0].m1_time

        if self.current_time_1 < time_1_player:
            self.current_time_1 += dt * 100
            
        else:
            self.current_time_1 = 0
            # change people

        ...
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
        self.draw_arc(draw_surface, self.start_platform_1, self.mid_platform_1)
        self.draw_arc(draw_surface, self.mid_platform_1, self.end_platform_1)
        self.draw_arc(draw_surface, self.start_platform_2, self.mid_platform_2)
        self.draw_arc(draw_surface, self.mid_platform_2, self.end_platform_2)

        #draw People
        self.people_player.x = map_value(self.current_time_1, 0, self.list_player[0].m1_time, self.start_platform_1.topright[0], self.mid_platform_1.topleft[0])
        pygame.draw.rect(draw_surface, BLUE, self.people_player)
    

    def draw_arc(self, draw_surface: pygame.Surface, start_plateform, end_plateform):
        # Size of the circles
        radius = 4
        
        # Height of the arc 
        arc_height = 0.1

        # Get the center points of the start and end platforms
        start_x = start_plateform.right
        start_y = start_plateform.top + radius
        end_x = end_plateform.left

        # Calculate the number of circles based on the distance between platforms
        num_circles = round((end_x - start_x) / 7)
        
        # Step size for the X positions
        step_x = (end_x - start_x) / (num_circles - 1)

        for i in range(num_circles):
            # Compute horizontal position (cx) at each step
            #cx = floor(start_x + i * step_x)

            # Normalize 'p' between 0 and 1
            p = i / (num_circles - 1)

            cy = arc_height*((2*p-1)**2) 
            # Draw the circle at the calculated position (cx, cy)
            pygame.draw.circle(draw_surface, BROWN, (cx, cy), radius)


    """
    def draw_arc(self, draw_surface: pygame.Surface, start_platform, end_platform):
        #size of the circle
        radius = 4
        
        # Get the center points of the start and end platforms
        start_x = start_platform.right
        start_y = start_platform.top+radius
        end_x = end_platform.left

        num_circles = round((end_x-start_x)/5.25)
        curve_height = 22
        step_x = (end_x - start_x) / (num_circles - 1)

        for i in range(num_circles):
            # Compute horizontal position
            cx = floor(start_x + i * step_x)

            # Create a curved shape using an inverted parabola
            t = i / (num_circles - 1)  # Normalize between 0 and 1
            cy = floor(start_y - (4 * curve_height * (t - 0.5) ** 2) + curve_height)

            # Draw the circle
            pygame.draw.circle(draw_surface, BROWN, (cx, cy), radius)
    """


