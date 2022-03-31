import pygame
from .utils import import_buttons

SCREEN_SIZE = (1280, 720)
BUTTON_IMAGE = import_buttons("/images/buttons/")

class Button(pygame.sprite.Sprite):
    def __init__(self, button_name: str, phase: str, posy: int, dimension: tuple):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.transform.scale(BUTTON_IMAGE[button_name], dimension)
       self.rect = self.image.get_rect()
       self.rect.center = (SCREEN_SIZE[0]//2, posy)
       self.phase = phase