import pygame
from abc import ABC, abstractmethod

class Scene(ABC):
    @abstractmethod
    def event_handler(self, event: pygame.Event, *args: list, **kwargs: dict) -> None:
        ...

    @abstractmethod
    def update(self, dt: float, *args: list, **kwargs: dict) -> None:
        ...

    @abstractmethod
    def draw(self, draw_surface: pygame.Surface, *args: list, **kwargs: dict) -> None:
        ...