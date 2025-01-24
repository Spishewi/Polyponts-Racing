import pygame

SCENE_CHANGE = pygame.event.custom_type()
def send_scene_change_event(scene: str):
    pygame.event.post(pygame.event.Event(SCENE_CHANGE, scene=scene))