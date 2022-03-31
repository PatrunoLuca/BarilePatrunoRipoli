import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.Surface, pos: tuple, speed: int):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(center= pos)
        self.speed = speed
        self.animation_speed = 0.3
        self.counter = 0
    
    def update(self):
        self.rect.y -= self.speed

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)