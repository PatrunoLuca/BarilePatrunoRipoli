from pygame.sprite import Sprite
from pygame import Surface


class MousePad(Sprite):
    def __init__(self, mouse_pos, mouse_buttons):
        Sprite.__init__(self)
        self.image = Surface([1, 1])
        self.image.fill('white')
        self.rect = self.image.get_rect(center= mouse_pos)
        self.left_pressed =  mouse_buttons[0]
    
    def update(self, mouse_pos, mouse_buttons):
        self.rect.center = mouse_pos
        self.left_pressed = mouse_buttons[0]
    
    def is_colliding_with_group(self, group, ):
        for i in group:
            if self.rect.colliderect(i.rect):
                return i.phase
        return False