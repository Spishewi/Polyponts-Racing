from scenes.scene import Scene
import pygame
from colors import *
from utils import People, map_value, bridge_parabolla, load_animation, RunningState
from algorithms.ia import sort_people, compute_total_time
import events

class PlayScene(Scene):

    def __init__(self, title_font: pygame.Font, text_font: pygame.Font, difficulty: str, people_list: list[People] ):
        #init difficulty and nb_people
        self.difficulty = difficulty
        self.people_list = people_list
        #window dimension
        window_height = pygame.display.get_surface().get_height()
        window_width = pygame.display.get_surface().get_width()
        dy = 160

        #init background image
        self.background_image = pygame.image.load('./assets/background.png').convert()
        self.background_image = pygame.transform.smoothscale(self.background_image, (window_width, self.background_image.get_height() * (window_height / self.background_image.get_height())))

        self.background_surface = pygame.Surface((window_width, window_height // 2))
        self.background_surface.blit(self.background_image, (0, - self.background_image.get_height() // 4))

        del self.background_image

        #init people image
        self.people_idle_frames = load_animation('./assets/idle/', 12, height=60, flip_x=True)
        self.people_run_frames = load_animation('./assets/run/', 10, height=60, flip_x=True)

        #init start platform
        self.start_platform_1 = pygame.Rect(0, dy, 115, window_height/2-dy)
        self.start_platform_2 = pygame.Rect(0, window_height/2+dy, 115, window_height/2-dy)

        #init mid platform
        self.mid_platform_1 = pygame.Rect(window_width/2-100, dy, 222, window_height/2-dy)
        self.mid_platform_2 = pygame.Rect(window_width/2-100, window_height/2+dy, 222, window_height/2-dy)

        #init finish plateform
        self.end_platform_1 = pygame.Rect(window_width-90, dy, 100, window_height/2-dy)
        self.end_platform_2 = pygame.Rect(window_width-90, window_height/2+dy, 100, window_height/2-dy)

        #init bridge consts
        self.bridge_circle_radius = 5
        self.bridge_step = 8
        self.bridge_height = 0.1

        #init list people
        self.bridge1_list_people_ia = sort_people(people_list, difficulty)
        self.bridge2_list_people_ia = []
        self.bridge1_list_people_player = people_list
        self.bridge2_list_people_player = []

        self.bridge1_current_time_ia = 0
        self.bridge2_current_time_ia = 0
        self.bridge1_current_time_player = 0
        self.bridge2_current_time_player = 0

        self.player_finished = False
        self.ia_finished = False
        self.remaining_people = (0, 0)

        #init people rect
        high_figure = 30
        self.people_player = pygame.Rect(self.start_platform_1.topright[0], self.start_platform_1.topright[1]-high_figure, 10, high_figure)
        
        #init font
        self.title_font = title_font
        self.text_font = text_font

        #init render
        self.title_render_player = self.text_font.render("Vos personnages :", True, BLACK)
        self.title_render_ia = self.text_font.render("Les personnages de l'IA :", True, BLACK)

        self.title_win_player = self.title_font.render("Vous avez gagné !", True, RED)
        self.title_win_ia = self.title_font.render("L'IA a gagné !", True, RED)
        self.title_win_draw = self.title_font.render("Egalité !", True, RED)

        
        self.next_btn_render = self.text_font.render("Résumé de la partie", True, BLACK)
        self.next_btn_rect  = pygame.Rect(window_width // 2 - self.next_btn_render.get_width() // 2 - 10, window_height - 80, self.next_btn_render.get_width() + 40, self.next_btn_render.get_height() + 20)

        #chrono init
        self.chrono_player = 0
        self.chrono_ia = 0
        self.current_time = 0

        # people name cache
        self.people_name_surface_cache = {}

        #final time ut
        self.final_time_ia = compute_total_time(self.bridge1_list_people_ia.copy())
        self.final_time_player = compute_total_time(self.bridge1_list_people_player.copy())
        
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_btn_rect.collidepoint(event.pos) and self.player_finished and self.ia_finished:

                events.send_scene_change_event("finish_scene", {
                    "final_time": (self.final_time_player, self.final_time_ia),
                    "number_people": self.remaining_people,
                    "has_win": self._get_has_win()
                })
   
    def update(self, dt: float, *args: list, **kwargs: dict):
        # player movement handling
        if len(self.bridge1_list_people_player) != 0:
            # someone is walking on the player bridge 1
            if self.bridge1_current_time_player < self.bridge1_list_people_player[0].m1_time:
                self.bridge1_current_time_player += dt * 15

            # someone has finished walking on the bridge 1
            else:
                self.bridge2_list_people_player.append(self.bridge1_list_people_player.pop(0))
                self.bridge1_current_time_player = 0

        if len(self.bridge2_list_people_player) != 0:
            if self.bridge2_current_time_player < self.bridge2_list_people_player[0].m2_time:
                self.bridge2_current_time_player += dt * 15
            else:
                self.bridge2_list_people_player.pop(0)
                self.bridge2_current_time_player = 0

        # ia movement handling
        if len(self.bridge1_list_people_ia) != 0:
            # someone is walking on the ia bridge 1
            if self.bridge1_current_time_ia < self.bridge1_list_people_ia[0].m1_time:
                self.bridge1_current_time_ia += dt * 15
            else:
                self.bridge2_list_people_ia.append(self.bridge1_list_people_ia.pop(0))
                self.bridge1_current_time_ia = 0
        
        if len(self.bridge2_list_people_ia) != 0:
            if self.bridge2_current_time_ia < self.bridge2_list_people_ia[0].m2_time:
                self.bridge2_current_time_ia += dt * 15
            else:
                self.bridge2_list_people_ia.pop(0)
                self.bridge2_current_time_ia = 0

        # check if the game is over
        if len(self.bridge1_list_people_player) == 0 and len(self.bridge2_list_people_player) == 0:
            self.player_finished = True

        if len(self.bridge1_list_people_ia) == 0 and len(self.bridge2_list_people_ia) == 0:
            self.ia_finished = True

        #if self.player_finished and not self.ia_finished:
        #    self.has_win = "player"
        #    self.remaining_people = (0, len(self.bridge1_list_people_ia) + len(self.bridge2_list_people_ia))

        #elif self.ia_finished and not self.player_finished:
        #    self.has_win = "ia"
        #    self.remaining_people = (len(self.bridge1_list_people_player) + len(self.bridge2_list_people_player), 0)

        #chrono update
        self.current_time += dt
        if not self.player_finished:
            self.chrono_player = self.current_time

        if not self.ia_finished:
            self.chrono_ia = self.current_time
            
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict):
        draw_surface.fill((255,255,255))
       
        #window dimension and useful things
        window_height = pygame.display.get_surface().get_height()
        window_width = pygame.display.get_surface().get_width()

        #draw background
        draw_surface.blit(self.background_surface, (0, 0))
        draw_surface.blit(self.background_surface, (0, window_height // 2))

        #draw line
        line_middle = pygame.Rect(0, window_height/2, window_width, 5)
        pygame.draw.rect(draw_surface, BLACK, line_middle)

        """
        #draw middle plateform
        pygame.draw.rect(draw_surface, GREY, self.mid_platform_1)
        pygame.draw.rect(draw_surface, GREY, self.mid_platform_2) 

        #draw end plateform
        pygame.draw.rect(draw_surface, GREY, self.end_platform_1)
        pygame.draw.rect(draw_surface, GREY, self.end_platform_2)"""

        #draw bridge
        self._draw_bridge(draw_surface, self.start_platform_1, self.mid_platform_1)
        self._draw_bridge(draw_surface, self.start_platform_1, self.mid_platform_1)
        self._draw_bridge(draw_surface, self.mid_platform_1, self.end_platform_1)
        self._draw_bridge(draw_surface, self.start_platform_2, self.mid_platform_2)
        self._draw_bridge(draw_surface, self.mid_platform_2, self.end_platform_2)

        #draw People
        if len(self.bridge1_list_people_player) > 0:
            self._draw_people(draw_surface, self.start_platform_1, self.mid_platform_1, self.bridge1_list_people_player[0].m1_time, self.bridge1_current_time_player, self.bridge1_list_people_player[0].id_number)
        if len(self.bridge1_list_people_ia) > 0:
            self._draw_people(draw_surface, self.start_platform_2, self.mid_platform_2, self.bridge1_list_people_ia[0].m1_time, self.bridge1_current_time_ia, self.bridge1_list_people_ia[0].id_number)

        if len(self.bridge2_list_people_player) > 0:
            self._draw_people(draw_surface, self.mid_platform_1, self.end_platform_1, self.bridge2_list_people_player[0].m2_time, self.bridge2_current_time_player, self.bridge2_list_people_player[0].id_number)
        if len(self.bridge2_list_people_ia) > 0:
            self._draw_people(draw_surface, self.mid_platform_2, self.end_platform_2, self.bridge2_list_people_ia[0].m2_time, self.bridge2_current_time_ia, self.bridge2_list_people_ia[0].id_number)

        #draw queue
        self._draw_queue(draw_surface, self.start_platform_1, self.bridge1_list_people_player)
        self._draw_queue(draw_surface, self.mid_platform_1, self.bridge2_list_people_player)
        self._draw_queue(draw_surface, self.start_platform_2, self.bridge1_list_people_ia)
        self._draw_queue(draw_surface, self.mid_platform_2, self.bridge2_list_people_ia)

        draw_surface.blit(self.title_render_player, self.title_render_player.get_rect(center=(window_width // 2, 30)))
        draw_surface.blit(self.title_render_ia, self.title_render_ia.get_rect(center=(window_width // 2, window_height//2 + 30)))

        #draw chronometer
        dx = 100
        dy = 20
        chrono_render_player = self.text_font.render(f"Chrono: {self.chrono_player:.2f}s", True, BLACK)
        draw_surface.blit(chrono_render_player, chrono_render_player.get_rect(center=(window_width-dx, dy)))

        chrono_render_ia = self.text_font.render(f"Chrono: {self.chrono_ia:.2f}s", True, BLACK)
        draw_surface.blit(chrono_render_ia, chrono_render_ia.get_rect(center=(window_width-dx, window_height/2+dy)))

        # WIN text
        if self.player_finished and not self.ia_finished:
            # black overlay
            BLACK_SURFACE = pygame.Surface((window_width, window_height//2))
            BLACK_SURFACE.set_alpha(100)
            draw_surface.blit(BLACK_SURFACE, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            # win text
            draw_surface.blit(self.title_win_player, self.title_win_player.get_rect(center=(window_width // 2, window_height//4)))

        if self.ia_finished and not self.player_finished:
            # black overlay
            BLACK_SURFACE = pygame.Surface((window_width, window_height//2))
            BLACK_SURFACE.set_alpha(100)
            draw_surface.blit(BLACK_SURFACE, (0, window_height//2), special_flags=pygame.BLEND_ALPHA_SDL2)
            # win text
            draw_surface.blit(self.title_win_ia, self.title_win_ia.get_rect(center=(window_width // 2, 3 * window_height//4)))

        # black overlay
        if self.player_finished and self.ia_finished:
            BLACK_SURFACE = pygame.Surface((window_width, window_height))
            BLACK_SURFACE.set_alpha(200)
            draw_surface.blit(BLACK_SURFACE, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

            if self._get_has_win() == "player":
                draw_surface.blit(self.title_win_player, self.title_win_player.get_rect(center=(window_width // 2, window_height//2)))
            elif self._get_has_win() == "ia":
                draw_surface.blit(self.title_win_ia, self.title_win_ia.get_rect(center=(window_width // 2, window_height//2)))
            else:
                draw_surface.blit(self.title_win_draw, self.title_win_draw.get_rect(center=(window_width // 2, window_height//2)))

            # next button
            pygame.draw.rect(draw_surface, BLUE, self.next_btn_rect, border_radius=5)
            draw_surface.blit(self.next_btn_render, self.next_btn_render.get_rect(center=self.next_btn_rect.center))
    def _draw_bridge(self, draw_surface: pygame.Surface, start_plateform: pygame.Rect, end_plateform: pygame.Rect):
        #set const
        
        scaley = end_plateform.left - start_plateform.right
        
        for i in range(int(start_plateform.right) + self.bridge_step // 2, int(end_plateform.left), self.bridge_step):
            y = start_plateform.top + self.bridge_circle_radius // 2 + bridge_parabolla(self.bridge_height, map_value(i, start_plateform.right, end_plateform.left, 0, 1)) * scaley
            pygame.draw.circle(draw_surface, BROWN, (i, y), self.bridge_circle_radius)
            
    def _draw_people(self, draw_surface: pygame.Surface, start_plateform: pygame.Rect, end_plateform: pygame.Rect, m_time: float, current_time: float, people_id: int):
        #set const
        people_frame = self._get_people_animation_frame(people_id, RunningState.RUNNING)

        people_rect = people_frame.get_rect()

        people_rect.centerx = map_value(current_time, 0, m_time, start_plateform.right, end_plateform.left)

        # on the bridge
        scaley = end_plateform.left - start_plateform.right
        people_rect.bottom = start_plateform.top + bridge_parabolla(self.bridge_height, map_value(people_rect.centerx, start_plateform.right, end_plateform.left, 0, 1)) * scaley

        people_name_surface = self._get_people_name_surface(people_id)
        people_frame = self._get_people_animation_frame(people_id, RunningState.RUNNING)
        draw_surface.blit(people_frame, (people_rect.x, people_rect.y + 10))
        draw_surface.blit(people_name_surface, people_name_surface.get_rect(center=pygame.Vector2(people_rect.center) + pygame.Vector2(0, -50)))


    def _get_people_animation_frame(self, people_id: int, running_state: RunningState):
        ticks = pygame.time.get_ticks()
        if running_state == RunningState.RUNNING:
            frame_number = (ticks // 100 + people_id) % len(self.people_run_frames)
            frame = self.people_run_frames[frame_number]
        else:
            frame_number = (ticks // 100 + people_id) % len(self.people_idle_frames)
            frame = self.people_idle_frames[frame_number]

        return frame
    def _draw_queue(self, draw_surface: pygame.Surface, start_plateform: pygame.Rect, queue: list):
        #set const
        spacing = 15

        if len(queue) <= 1:
            return
        
        # draw waiting people
        for i in range(len(queue)-1 , 0, -1):
            people_id = queue[i].id_number

            people_frame = self._get_people_animation_frame(people_id, RunningState.IDLE)
            people_rect = people_frame.get_rect()

            people_rect.centerx = start_plateform.right - i * spacing
            people_rect.bottom = start_plateform.top

            people_name_surface = self._get_people_name_surface(people_id)

            draw_surface.blit(people_frame, (people_rect.x, people_rect.y + 10))
            draw_surface.blit(people_name_surface, people_name_surface.get_rect(center=pygame.Vector2(people_rect.center) + pygame.Vector2(0, -50)))
    def _get_people_name_surface(self, id_number: int):
        if id_number in self.people_name_surface_cache:
            return self.people_name_surface_cache[id_number]
        else:
            people_name_surface = self.text_font.render(chr(ord("A") + id_number - 1), True, BLACK)
            self.people_name_surface_cache[id_number] = people_name_surface
            return people_name_surface
        
    def _get_has_win(self) -> str | None:
        if self.final_time_ia < self.final_time_player:
            return "ia"
        if self.final_time_player < self.final_time_ia:
            return "player"
        return None