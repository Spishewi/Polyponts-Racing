from dataclasses import dataclass
@dataclass(frozen=True)
class People:
    id_number: int
    m1_time: int
    m2_time: int

import pygame
from colors import *


def map_value(value, min1, max1, min2, max2):
    """
    Maps a value from one range to another range.

    Args:
        value (float): The value to be mapped.
        min1 (float): The minimum of the first range.
        max1 (float): The maximum of the first range.
        min2 (float): The minimum of the second range.
        max2 (float): The maximum of the second range.

    Returns:
        float: The mapped value.
    """
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2

def bridge_parabolla(height: float, t: float):
    return - height * (2 * t - 1) ** 2 + height

def multiple_render(text: str, font: pygame.font):
    list_render =[]
    for word in text.split():
        word_render = font.render(word, True, BLACK)
        list_render.append(word_render)
    return list_render