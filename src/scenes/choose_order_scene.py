from scenes.scene import Scene
import pygame 
from colors import *
import events

from utils import map_value, People
from math import floor, ceil

from random import randint, shuffle

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

        draw_surface = pygame.display.get_surface() # not perfect, but it's more performant.

        #init button play
        self.play_button_render = self.text_font.render("Jouer !", True, BLACK)
        self.play_button = pygame.Rect(draw_surface.width // 2 - self.play_button_render.width, draw_surface.height - 80, 120, 60)
        #init button back
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        #order table renders
        self.name_label_render = self.text_font.render("Nom fourmi", True, BLACK)
        self.m1_time_render = self.text_font.render("Temps pont 1", True, BLACK)
        self.m2_time_render = self.text_font.render("Temps pont 2", True, BLACK)

        #order table rects
        self.table_line_width = 2
        self.table_first_col_width = 180

        self.table_rect_1 = pygame.Rect(25, 150, draw_surface.width - 50, draw_surface.height // 4)
        self.table_rect_2 = pygame.Rect(25, self.table_rect_1.bottom + 10, draw_surface.width - 50, draw_surface.height // 4)

        # generate cells renders
        self.people_list = self._generate_people_list()
        self.cells_list = self._generate_cells_list()

        # cell grabbing
        self.grabbed_cell_index = None


    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                events.send_scene_change_event("choose_number_scene", {
                                                   "difficulty":self.difficulty,
                                                    "nb_people":self.nb_people
                                                })
                
            elif self.play_button.collidepoint(event.pos):
                events.send_scene_change_event("play_scene",{
                                                    "difficulty": self.difficulty,
                                                    "people_list": self.people_list
                                                })
                
            elif (cell_index := self._get_collided_cell(event)) != None:
                self.grabbed_cell_index = cell_index

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (cell_index := self._get_collided_cell(event)) is not None and self.grabbed_cell_index is not None:
                self.cells_list[cell_index], self.cells_list[self.grabbed_cell_index] = self.cells_list[self.grabbed_cell_index], self.cells_list[cell_index]
                self.people_list[cell_index], self.people_list[self.grabbed_cell_index] = self.people_list[self.grabbed_cell_index], self.people_list[cell_index]

            self.grabbed_cell_index = None

                
    def update(self, dt: float, *args: list, **kwargs: dict):
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255, 255, 255))
        window_width = draw_surface.width
        window_height = draw_surface.height
        
        #draw title
        draw_surface.blit(self.title_render_1, self.title_render_1.get_rect(center=(window_width // 2, 30)))
        draw_surface.blit(self.title_render_2, self.title_render_2.get_rect(center=(window_width // 2, 60)))
        
        #draw button back
        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))
        
        #draw table
        self._draw_table_content(draw_surface)
        self._draw_table_hover(draw_surface)
        self._draw_table_border(draw_surface)

        # draw grabbed cell
        if self.grabbed_cell_index is not None:
            self._draw_grabbed_cell(draw_surface)


        #draw button play
        pygame.draw.rect(draw_surface, ORANGE, self.play_button, border_radius=5)
        draw_surface.blit(self.play_button_render, self.play_button_render.get_rect(center=self.play_button.center))

    def _draw_table_hover(self, draw_surface: pygame.Surface):
        ...
    def _draw_table_content(self, draw_surface: pygame.Surface):
        for i, cell in enumerate(self.cells_list):
            
            draw_surface.blit(cell, self._get_cell_position(i, cell))

    def _draw_table_border(self, draw_surface: pygame.Surface):
        
        # to not use self everywere
        line_width = self.table_line_width
        first_col_width = self.table_first_col_width

        table_rect_1 = self.table_rect_1
        table_rect_2 = self.table_rect_2

        # draw lines
        for i in range(2):
            pygame.draw.line(draw_surface, BLACK,
                             (table_rect_1.left, table_rect_1.top + (i+1)*table_rect_1.height/3),
                             (table_rect_1.left + first_col_width, table_rect_1.top + (i+1)*table_rect_1.height/3),
                             width=line_width)
            
        for i in range(10):
            pygame.draw.line(draw_surface, BLACK,
                             (table_rect_1.left + first_col_width + i*(table_rect_1.width - first_col_width)/10, table_rect_1.top),
                             (table_rect_1.left + first_col_width + i*(table_rect_1.width - first_col_width)/10, table_rect_1.bottom - line_width),
                             width=line_width)
            
        for i in range(2):
            pygame.draw.line(draw_surface, BLACK,
                             (table_rect_2.left, table_rect_2.top + (i+1)*table_rect_2.height/3),
                             (table_rect_2.left + first_col_width, table_rect_2.top + (i+1)*table_rect_2.height/3),
                             width=line_width)
            
        for i in range(10):
            pygame.draw.line(draw_surface, BLACK,
                             (table_rect_2.left + first_col_width + i*(table_rect_2.width - first_col_width)/10, table_rect_2.top),
                             (table_rect_2.left + first_col_width + i*(table_rect_2.width - first_col_width)/10, table_rect_2.bottom - line_width),
                             width=line_width)
            

        draw_surface.blit(self.name_label_render, (table_rect_1.left + 5, table_rect_1.top + 5))
        draw_surface.blit(self.m1_time_render, (table_rect_1.left + 5, table_rect_1.top + table_rect_1.height // 3 + 5))
        draw_surface.blit(self.m2_time_render, (table_rect_1.left + 5, table_rect_1.top + 2 * table_rect_1.height // 3 + 5))

        draw_surface.blit(self.name_label_render, (table_rect_2.left + 5, table_rect_2.top + 5))
        draw_surface.blit(self.m1_time_render, (table_rect_2.left + 5, table_rect_2.top + table_rect_2.height // 3 + 5))
        draw_surface.blit(self.m2_time_render, (table_rect_2.left + 5, table_rect_2.top + 2 * table_rect_2.height // 3 + 5))
            
            
        pygame.draw.rect(draw_surface, BLACK, table_rect_1, width=2, border_radius=5)
        pygame.draw.rect(draw_surface, BLACK, table_rect_2, width=2, border_radius=5)

    def _draw_grabbed_cell(self, draw_surface: pygame.Surface):
        # get grabbed cell
        cell: pygame.Surface = self.cells_list[self.grabbed_cell_index]
        # draw grabbed cell

        alpha_surface_without_corners = pygame.Surface(cell.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(alpha_surface_without_corners, WHITE, alpha_surface_without_corners.get_rect(), border_radius=5)

        cell_without_corners = cell.copy().convert_alpha()
        cell_without_corners.blit(alpha_surface_without_corners, special_flags=pygame.BLEND_RGBA_MIN)

        draw_surface.blit(cell_without_corners, cell.get_rect(center=pygame.mouse.get_pos()))

        # put a box around
        pygame.draw.rect(draw_surface, BLACK, cell.get_rect(center=pygame.mouse.get_pos()), width=2, border_radius=5)

    def _generate_people_list(self) -> list[People]:
        return [People(i, randint(4, 14)*10, randint(6, 16)*10) for i in range(1, self.nb_people + 1)]
    
    def _generate_cells_list(self) -> list[pygame.Surface]:
        cells = []
        for people in self.people_list:
            cell_surface = pygame.Surface(((self.table_rect_1.width - self.table_first_col_width)/10, self.table_rect_1.height))
            cell_surface.fill(WHITE)

            cell_id_render = self.text_font.render(chr(ord("A") + people.id_number - 1), True, BLACK)
            cell_time1_render = self.text_font.render(str(people.m1_time), True, BLACK)
            cell_time2_render = self.text_font.render(str(people.m2_time), True, BLACK)

            cell_surface_rect = cell_surface.get_rect()
            cell_surface.blit(cell_id_render, cell_id_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery - cell_surface_rect.height//3)))
            cell_surface.blit(cell_time1_render, cell_time1_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery)))
            cell_surface.blit(cell_time2_render, cell_time2_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery + cell_surface_rect.height//3)))
            
            pygame.draw.line(cell_surface, BLACK, (0, cell_surface.height/3), (cell_surface.width, cell_surface.height/3), width=2)
            pygame.draw.line(cell_surface, BLACK, (0, cell_surface.height*2/3), (cell_surface.width, cell_surface.height*2/3), width=2)
            cells.append(cell_surface)
        return cells
    
    def _get_cell_position(self, i: int, cell: pygame.Surface) -> pygame.typing.Point:
        x = self.table_rect_1.x + self.table_first_col_width + (i%10)*cell.width
        y = self.table_rect_1.y if i // 10 == 0 else self.table_rect_2.y

        return (x, y)
    def _get_collided_cell(self, event: pygame.Event) -> int | None:
        for i, cell in enumerate(self.cells_list):
            if self.grabbed_cell_index is not None and cell is self.cells_list[self.grabbed_cell_index]:
                continue
            cell : pygame.surface
            if cell.get_rect(topleft=self._get_cell_position(i, cell)).collidepoint(event.pos):
                return i
        return None