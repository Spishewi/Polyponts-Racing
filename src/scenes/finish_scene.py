from scenes.scene import Scene
import pygame
from colors import *
import events

class FinishScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, final_time: tuple[int, int], number_people: tuple[int, int], has_win: str):
        window_width = pygame.display.get_surface().get_width()
        window_height = pygame.display.get_surface().get_height()

        #init font
        self.title_font = title_font
        self.text_font = text_font
        
        #init title
        self.title_render = title_font.render("Résultat", True, BLACK)

        #init button finish
        self.button_render = text_font.render("Rejouer", True, BLACK)
        self.finish_button = pygame.Rect(window_width//2-self.button_render.get_width()/2, window_height-120, window_width/6, window_width/10)
        
        #init win render
        if has_win == "player":
            has_win ="gagné"
        else:
            has_win = "perdu"
        self.has_win_render = text_font.render(f"Vous avez {has_win}", True, BLACK)

        #init grid
        self.grid = pygame.Rect(75, 150, window_width - 150, window_height - 320)
        self.number_rows = 2
        self.number_columns = 4

        #init text line
        self.player_render = text_font.render("Joueur", True, BLACK)
        self.ia_render = text_font.render("IA", True, BLACK)

        #init text column
        self.final_time_render = text_font.render("Temps final", True, BLACK)
        self.diff_time_render1 = text_font.render("Différence", True, BLACK)
        self.diff_time_render2 = text_font.render("de temps", True, BLACK)
        self.people_remaning1 = text_font.render("Nombre de", True, BLACK)
        self.people_remaning2 = text_font.render("personnes ", True, BLACK)
        self.people_remaning3 = text_font.render("restantes", True, BLACK)

        #init grid value
        self.final_time = final_time
        self.number_people = number_people

        if self.final_time[0] <= self.final_time[1]:
            self.final_time_render_player = text_font.render(f"{self.final_time[0]:.2f}s", True, GREEN)
            self.final_time_render_ia = text_font.render(f"{self.final_time[1]:.2f}s", True, RED)
            self.diff_time_player_render = text_font.render("0", True, GREEN)
            self.diff_time_ia_render = text_font.render(f"+{(self.final_time[1] - self.final_time[0]):.2f}s", True, RED)
            
        else:
            self.final_time_render_player = text_font.render(f"{self.final_time[0]:.2f}s", True, RED)
            self.final_time_render_ia = text_font.render(f"{self.final_time[1]:.2f}s", True, GREEN)
            self.diff_time_player_render = text_font.render(f"+{(self.final_time[0] - self.final_time[1]):.2f}s", True, RED)
            self.diff_time_ia_render = text_font.render("0", True, GREEN)
        
        self.number_people_player_render = text_font.render(str(self.number_people[0]), True, BLACK)
        self.number_people_ia_render = text_font.render(str(self.number_people[1]), True, BLACK) 


    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        #change the scene according to the mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.finish_button.collidepoint(event.pos):
                events.send_scene_change_event("mainmenu")

        
    def update(self, dt: float, *args: list, **kwargs: dict):

        ...
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill(BACKGROUND_COLOR)
        window_width = draw_surface.get_width()
        
        #draw title
        draw_surface.blit(self.title_render, self.title_render.get_rect(center=(window_width // 2, 30)))

        #draw button 
        pygame.draw.rect(draw_surface, ORANGE, self.finish_button, border_radius=5)
        draw_surface.blit(self.button_render, self.button_render.get_rect(center=self.finish_button.center))

        #draw win text
        draw_surface.blit(self.has_win_render, self.has_win_render.get_rect(center=(window_width // 2, 100)))

        #draw grid with text
        pygame.draw.rect(draw_surface, BLACK, self.grid, border_radius=5, width=2)
        self._draw_grid_border(draw_surface)

    def _draw_grid_border(self, draw_surface):

        #set characteristic of the grid
        nb_lines = 3
        nb_columns = 4
        y_start_row = 100
        x_start_column = 160
        
        #draw row
        x_end_row = self.grid.x + self.grid.width
        first_line_row = self.grid.y + y_start_row
        #draw first line 
        pygame.draw.line(
            draw_surface, BLACK, (self.grid.x, first_line_row), (x_end_row, first_line_row), width=2
        )
        row_spacing = (self.grid.height - y_start_row) / (nb_lines-1)
        for i in range(1,nb_lines-1):
            y = first_line_row + row_spacing*i
            pygame.draw.line(
                draw_surface, BLACK, (self.grid.x, y), (x_end_row, y), width=2
            )

        #draw column
        y_end_column = self.grid.y + self.grid.height
        first_line_column = self.grid.x + x_start_column
        #draw first cline column
        pygame.draw.line(
            draw_surface, BLACK, (first_line_column, self.grid.y), (first_line_column, y_end_column), width=2
        )
        column_spacing = (self.grid.width - x_start_column) / (nb_columns-1)
        for i in range(1,nb_columns-1):
            x = first_line_column + column_spacing * i
            pygame.draw.line(
                draw_surface, BLACK, (x, self.grid.y), (x, y_end_column), width=2
            )
        
        #draw text of the lines
        self._draw_grid_content(draw_surface, [self.player_render], (self.grid.x, first_line_row), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.ia_render], (self.grid.x, first_line_row+row_spacing ), column_spacing, row_spacing)

        #draw text of the columns
        self._draw_grid_content(draw_surface, [self.final_time_render], (first_line_column, self.grid.y), column_spacing, row_spacing )
        self._draw_grid_content(draw_surface, [self.diff_time_render1, self.diff_time_render2], (first_line_column+column_spacing, self.grid.y), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.people_remaning1,self.people_remaning2,self.people_remaning3], (first_line_column+column_spacing*2, self.grid.y), column_spacing, row_spacing)

        #draw values of the grid
        self._draw_grid_content(draw_surface,[self.final_time_render_player], (first_line_column, first_line_row), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.final_time_render_ia], (first_line_column, first_line_row+row_spacing), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.diff_time_player_render], (first_line_column+column_spacing, first_line_row), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.diff_time_ia_render], (first_line_column+column_spacing, first_line_row+row_spacing), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.number_people_player_render], (first_line_column+column_spacing*2, first_line_row), column_spacing, row_spacing)
        self._draw_grid_content(draw_surface, [self.number_people_ia_render], (first_line_column+column_spacing*2, first_line_row+row_spacing), column_spacing, row_spacing)
   
    def _draw_grid_content(self, draw_surface, text_render:list[pygame.Surface], top_position:tuple[int, int], width_rect:int, height_rect:int):
        #calculate the center of the rect
        center_x = top_position[0] + width_rect / 2
        center_y = top_position[1] + height_rect / 2
        y_gap = 10

        if len(text_render)==1:
            first_text_y = center_y - sum(render.get_height() for render in text_render) / 2  
        else:
            first_text_y = center_y - sum(render.get_height() for render in text_render) / 2 + y_gap

        for render in text_render:
            text_x = center_x - render.get_width() / 2
            draw_surface.blit(render, (text_x, first_text_y))
            first_text_y += y_gap + render.get_height()/2
            
