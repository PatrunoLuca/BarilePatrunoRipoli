from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import surface
from .retta import Retta

# Classe proiettile
class Bullet(Sprite):
    # Prendi in input l'immagine del proiettile, la cordinata
    # sull'asse x, quella sull'asse y, la velocità del 
    # proiettile e se esso ruota o no
    def __init__(self, image: surface, posx: int, posy: int, is_rotating: bool, destroy_at_collision: bool, direction="down"):
        super().__init__()
        # Salvo i parametri di init
        assert direction in ["down", "up", "left", "right"]
        self.surface = image
        #self.posy = posy
        self.is_rotating = is_rotating
        self.destroy_at_collision = destroy_at_collision
        
        self.angle = 0
        if not is_rotating:
            if direction == "right":
                self.angle = 90
            elif direction == "up":
                self.anegle = 180
            elif direction == "left":
                self.angle = 270

        self.image = rotate(self.surface, self.angle)
        
        # Creo un oggetto retta che rappresenta il moto
        # del proiettile nel piano e trovo la lista di punti
        # che giace nel piano
        if direction == "down":
            self.posx = posx - (self.image.get_width()/2) if not rotate else posx - (self.image.get_width()/2) -10
            self.retta = Retta(self.posx, 0, 0)
            self.punti = self.retta.coppie(posy, 850,  1)
        elif direction == "right":
            self.posy = posy - (self.image.get_height()/2) if not rotate else posy - (self.image.get_height()/2) - 10
            self.retta = Retta(0, self.posy, posx)
            self.punti = self.retta.coppie(posx, 1400, 1)
        elif direction == "left":
            self.posy = posy - (self.image.get_height()/2) if not rotate else posy - (self.image.get_height()/2) -10
            self.retta = Retta(0, self.posy, posx)
            self.punti = self.retta.coppie(posx, -200,-1)

        self.rect = self.image.get_rect(center=(posx, posy))
        # Setto tutte le variabili di base del proiettile
        self.counter = 0

    def update(self):
        # Aggiorno la posizione del proiettile utilizzando
        # i punti presi grazie alla retta
        self.rect.x = self.punti[self.counter][0]
        self.rect.y = self.punti[self.counter][1]
        
        # Il contatore aumenta se ci sono altri punti
        # nella lista
        if len(self.punti) > (self.counter + 5):
            self.counter += 5
        
        # Se il proiettile deve ruotare allora aumenta 
        # l'angolo di 20 gradi è imposta lo sprite ruotato
        # dell'angolo attuale come immagine
        if self.is_rotating:
            self.angle += 15
            if self.angle > 360:
                self.angle = self.angle - 360
            self.image = rotate(self.surface, self.angle)

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
            
