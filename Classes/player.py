from .utils import import_animations, import_bullets
from pygame.sprite import Sprite, Group
from pygame.math import Vector2

# Classe del personaggio giocante
class Player(Sprite):
    # Il metodo init prende in input la posizione del
    # personaggio al momento della sua generazione
    def __init__(self, pos: tuple):
        super().__init__()
        
        # Importo la lista di tutte le animazioni del protagonista
        self.animations = import_animations("images/character/",128,128)
        
        self.image = self.animations["idle"][0]
        self.vector = Vector2(0, 0)
        self.rect = self.image.get_rect(center= pos)
        
        # Setto tutte le variabili di base del personaggio
        self.speed = 5
        self.animation_speed = 0.3
        self.counter = 0
        self.old_animation = "idle"

    def update(self):
        # Muovi il personaggio e aumenta il contatore
        # dell'animazione
        self.rect.x += self.vector.x * self.speed
        self.rect.y += self.vector.y * self.speed
        self.counter += self.animation_speed

        # Se l'animazione è finita falla ricominciare da capo
        if self.counter >= len(self.animations[self.old_animation]):
            self.counter = 0

        # Se cambia l'animazione allora imposta il contatore
        # dell'animazione a 0.7
        if self.new_animation != self.old_animation:
            self.counter = 0.7

        self.old_animation = self.new_animation
        # Imposta il frame dall'animazione attuale
        self.image = self.animations[self.new_animation][int(self.counter)] 
