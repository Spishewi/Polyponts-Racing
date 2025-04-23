from scenes.scene import Scene
import pygame 
from colors import *
import events

from utils import People
from random import randint

from algorithms.ia import compute_total_time

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
        draw_surface_width = draw_surface.get_width()
        draw_surface_height = draw_surface.get_height()

        #init button play
        self.play_button_render = self.text_font.render("Jouer !", True, BLACK)
        self.play_button = pygame.Rect(draw_surface_width // 2 - self.play_button_render.get_width()//2, draw_surface_height - 80, 120, 60)
        #init button back
        self.back_button_render = self.text_font.render("Retour", True, BLACK)
        self.back_button = pygame.Rect(10, 10, 100, 50)

        #order table renders
        self.name_label_render = self.text_font.render("Nom", True, BLACK)
        self.m1_time_render = self.text_font.render("Temps pont 1", True, BLACK)
        self.m2_time_render = self.text_font.render("Temps pont 2", True, BLACK)

        #order table rects
        self.table_line_width = 2
        self.table_first_col_width = 180

        self.table_rect_1 = pygame.Rect(25, 150, draw_surface_width - 50, draw_surface_height // 4)
        self.table_rect_2 = pygame.Rect(25, self.table_rect_1.bottom + 10, draw_surface_width - 50, draw_surface_height // 4)

        # generate cells renders
        self.people_list = self._generate_people_list()
        self.cells_list = self._generate_cells_list()

        self._updated_computed_total_time()

        # cell grabbing
        self.grabbed_cell_index = None
        self.collided_cell_index = None


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
            if (collided_cell_index := self._get_collided_cell(event)) is not None and self.grabbed_cell_index is not None:
                
                #self.cells_list[cell_index], self.cells_list[self.grabbed_cell_index] = self.cells_list[self.grabbed_cell_index], self.cells_list[cell_index]
                #self.people_list[cell_index], self.people_list[self.grabbed_cell_index] = self.people_list[self.grabbed_cell_index], self.people_list[cell_index]
                self.cells_list.insert(collided_cell_index, self.cells_list.pop(self.grabbed_cell_index))
                self.people_list.insert(collided_cell_index, self.people_list.pop(self.grabbed_cell_index))

                self._updated_computed_total_time()

            self.grabbed_cell_index = None

        elif event.type == pygame.MOUSEMOTION:
            if (collided_cell_index := self._get_collided_cell(event)) is not None and self.grabbed_cell_index is not None:
                self.collided_cell_index = collided_cell_index
            else:
                self.collided_cell_index = None

                
    def update(self, dt: float, *args: list, **kwargs: dict):
        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill(BACKGROUND_COLOR)
        window_width = draw_surface.get_width()
        window_height = draw_surface.get_height()
        
        #draw title
        draw_surface.blit(self.title_render_1, self.title_render_1.get_rect(center=(window_width // 2, 35)))
        draw_surface.blit(self.title_render_2, self.title_render_2.get_rect(center=(window_width // 2, 65)))
        
        #draw button back
        pygame.draw.rect(draw_surface, GREY, self.back_button, border_radius=5)
        draw_surface.blit(self.back_button_render, self.back_button_render.get_rect(center=self.back_button.center))
        
        #draw table
        self._draw_table_content(draw_surface)
        self._draw_table_border(draw_surface)
        self._draw_table_grabbed_overlay(draw_surface)

        # draw grabbed cell
        if self.grabbed_cell_index is not None:
            self._draw_grabbed_cell(draw_surface)

        #draw computed time
        if self.difficulty == "easy":
            draw_surface.blit(self.render_total_computed_time, self.render_total_computed_time.get_rect(center=self.play_button.center + pygame.Vector2(0, -70)))


        #draw button play
        pygame.draw.rect(draw_surface, CARIBBEAN_CURRENT, self.play_button, border_radius=5)
        draw_surface.blit(self.play_button_render, self.play_button_render.get_rect(center=self.play_button.center))

    def _draw_table_grabbed_overlay(self, draw_surface: pygame.Surface):
        # drawing the line
        if self.grabbed_cell_index is not None and self.collided_cell_index is not None:
            collided_cell = self.cells_list[self.collided_cell_index]
            collided_cell_pos = self._get_cell_position(self.collided_cell_index, collided_cell)
            
            # if the line is on the left
            if (self.collided_cell_index - self.grabbed_cell_index) < 0:
                start_pos = collided_cell_pos
                end_pos = collided_cell_pos + pygame.Vector2(0, collided_cell.get_height() - 1)
                pygame.draw.line(draw_surface, CARIBBEAN_CURRENT, start_pos, end_pos, 3)
            # if the line is on the right
            elif (self.collided_cell_index - self.grabbed_cell_index) > 0:
                start_pos = collided_cell_pos + pygame.Vector2(collided_cell.get_width(), 0)
                end_pos = collided_cell_pos + pygame.Vector2(collided_cell.get_width(), collided_cell.get_height()- 1)
                pygame.draw.line(draw_surface, CARIBBEAN_CURRENT, start_pos, end_pos, 3)

    def _draw_table_content(self, draw_surface: pygame.Surface):
        
        for i, cell in enumerate(self.cells_list):
            if self.grabbed_cell_index is not None and i == self.grabbed_cell_index:
                continue
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
        cell_without_corners.blit(alpha_surface_without_corners, dest=(0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        draw_surface.blit(cell_without_corners, cell.get_rect(center=pygame.mouse.get_pos()))

        # put a box around
        pygame.draw.rect(draw_surface, BLACK, cell.get_rect(center=pygame.mouse.get_pos()), width=2, border_radius=5)

    def _generate_people_list(self) -> list[People]:
        return [People(i, randint(1, 10)*10, randint(2, 12)*10) for i in range(1, self.nb_people + 1)]
    
    def _generate_cells_list(self) -> list[pygame.Surface]:
        cells = []
        for people in self.people_list:
            cell_surface = pygame.Surface(((self.table_rect_1.width - self.table_first_col_width)/10, self.table_rect_1.height))
            cell_surface.fill(BACKGROUND_COLOR)

            cell_id_render = self.text_font.render(chr(ord("A") + people.id_number - 1), True, BLACK)
            cell_time1_render = self.text_font.render(str(people.m1_time), True, BLACK)
            cell_time2_render = self.text_font.render(str(people.m2_time), True, BLACK)

            cell_surface_rect = cell_surface.get_rect()
            cell_surface.blit(cell_id_render, cell_id_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery - cell_surface_rect.height//3)))
            cell_surface.blit(cell_time1_render, cell_time1_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery)))
            cell_surface.blit(cell_time2_render, cell_time2_render.get_rect(center=(cell_surface_rect.centerx, cell_surface_rect.centery + cell_surface_rect.height//3)))
            
            pygame.draw.line(cell_surface, BLACK, (0, cell_surface.get_height()/3), (cell_surface.get_width(), cell_surface.get_height()/3), width=2)
            pygame.draw.line(cell_surface, BLACK, (0, cell_surface.get_height()*2/3), (cell_surface.get_width(), cell_surface.get_height()*2/3), width=2)
            cells.append(cell_surface)
        return cells
    
    def _get_cell_position(self, i: int, cell: pygame.Surface) -> pygame.Vector2:
        x = self.table_rect_1.x + self.table_first_col_width + (i%10)*cell.get_width()
        y = self.table_rect_1.y if i // 10 == 0 else self.table_rect_2.y

        return pygame.Vector2(x, y)
    def _get_collided_cell(self, event: pygame.Event) -> int | None:
        for i, cell in enumerate(self.cells_list):
            if self.grabbed_cell_index is not None and cell is self.cells_list[self.grabbed_cell_index]:
                continue
            cell : pygame.surface
            if cell.get_rect(topleft=self._get_cell_position(i, cell)).collidepoint(event.pos):
                return i
        return None
    
    def _updated_computed_total_time(self):
        self.total_computed_time = compute_total_time(self.people_list.copy())
        self.render_total_computed_time = self.text_font.render(f"Temps total de traversée : {self.total_computed_time} UT.", True, BLACK)

