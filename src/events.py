import pygame

SCENE_CHANGE = pygame.event.custom_type()
def send_scene_change_event(scene: str, **kwargs: dict):
    pygame.event.post(pygame.event.Event(SCENE_CHANGE, scene=scene, **kwargs))