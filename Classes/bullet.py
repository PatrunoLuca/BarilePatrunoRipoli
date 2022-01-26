from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import surface
from .retta import Retta

# Classe proiettile
class Bullet(Sprite):
    # Prendi in input l'immagine del proiettile, la cordinata
    # sull'asse x, quella sull'asse y, la velocità del 
    # proiettile e se esso ruota o no
    def __init__(self, image: surface, posx: int, posy: int, rotate: bool, destroy_at_collision: bool):
        super().__init__()
        # Salvo i parametri di init
        self.surface = image
        self.posx = posx
        self.posy = posy
        self.rotate = rotate
        self.destroy_at_collision = destroy_at_collision
        
        # Creo un oggetto retta che rappresenta il moto
        # del proiettile nel piano e trovo la lista di punti
        # che giace nel piano
        self.retta = Retta(posx, 0, 0)
        self.punti = self.retta.coppie(posy, 850,  +1)
        
        self.image = image
        self.rect = self.image.get_rect(center=self.punti[0])
        # Setto tutte le variabili di base del proiettile
        self.counter = 0
        self.angle = 0

    def update(self):
        # Aggiorno la posizione del proiettile utilizzando
        # i punti presi grazie alla retta
        self.rect.x = self.punti[self.counter][0]
        self.rect.y = self.punti[self.counter][1]
        
        # Il contatore aumenta se ci sono altri punti
        # nella lista
        if len(self.punti) > (self.counter + 10):
            self.counter += 10
        
        # Se il proiettile deve ruotare allora aumenta 
        # l'angolo di 20 gradi è imposta lo sprite ruotato
        # dell'angolo attuale come immagine
        if self.rotate:
            self.angle += 20
            self.image = rotate(self.surface, self.angle)

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
            
