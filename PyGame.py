from random import randint

import pygame

from Classes.bullet import Bullet
from Classes.player import Player
from Classes.utils import import_bullets

SCREEN_SIZE = (800, 600)
PLAYER_POSITION = (400, 80)#(100, 300)
MAX_SHURIKEN_COOLDOWN = 30
MAX_KUNAI_COOLDOWN = 30
MAX_INVULNERABILITY_COOLDOWN = 60
MAX_ENEMY_SPAWN_COOLDOWN = 30
MAX_INCREASE_SPEED_COOLDOWN = 300
BULLETS_SPRITES = import_bullets("images/bullets/",64,64)
BULLET_SPEED = 10
ENEMY_HIT_POINTS = 100
KUNAI_POINTS = 10
SHURIKEN_POINTS = 10


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color: str, width: int, height: int, pos: tuple, speed: int):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect(center=pos)
       self.speed = speed
       #print(pygame.Rect(pos, 0, 0).inflate(height, width)==self.image.get_rect(center=pos))
    
    def update(self):
        if enemy_moving:
            self.rect.y -= self.speed

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

#Questa è la classe base che gestisce tutto il gioco
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.player = Player(PLAYER_POSITION)
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.run = True
        self.shuriken_cooldown = 0
        self.kunai_cooldown = 0
        self.invulnerability_cooldown = MAX_INVULNERABILITY_COOLDOWN
        self.enemy_spawn_cooldown = 10
        self.increase_speed_cooldwn = MAX_INCREASE_SPEED_COOLDOWN
        self.life = 2
        self.enemy_speed = 1
        self.enemy_passed = 0
        self.game_points = {
            "score" : 0,
            "enemy_killed" : 0,
            "shuriken_shooted" : 0,
            "kunai_shooted" : 0
        }

    def check_bullets(self):
        for bullet in self.bullet_group:
            typo = "shuriken" if bullet.rotate else "kunai"
            print(f"Bullet: {typo}\tSize: {bullet.image.get_size()}")
            if bullet.rect.y > 830:
                self.bullet_group.remove(bullet)

            for enemy in self.enemy_group:
                if bullet.is_collided_with(enemy):
                    self.enemy_group.remove(enemy)
                    self.game_points['score'] += ENEMY_HIT_POINTS
                    self.game_points['enemy_killed'] += 1
                    if bullet.destroy_at_collision:
                        self.bullet_group.remove(bullet)
                    print(f"Bullet: {bullet.rect.x}, {bullet.rect.y}\tEnemy: {enemy.rect.x}, {enemy.rect.y}")
    
    def check_enemies(self):
        for enemy in self.enemy_group:
            if enemy.rect.y < -10:
                self.enemy_passed += 1
                print("Enemy Passed!")
                self.enemy_group.remove(enemy)
            if enemy.is_collided_with(self.player) and self.invulnerability_cooldown == 0:
                self.life -=1
                print("Hai perso una vita!")
                self.invulnerability_cooldown = MAX_INVULNERABILITY_COOLDOWN
    
    def get_input(self):
        # Trovo i tasti che sono stati premuti facendo
        # muovere il personaggio nella direzione scelta 
        # scegliendo il tipo di animazione durante la camminata
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.rect.top > 0:
            self.player.new_animation = "down-run"
            self.player.vector.x = 0
            self.player.vector.y = -1
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.player.rect.bottom < 600:
            self.player.new_animation = "down-run"
            self.player.vector.x = 0
            self.player.vector.y = 1
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.player.rect.left > -19:
            self.player.new_animation = "down-run"
            self.player.vector.x = -1
            self.player.vector.y = 0
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.player.rect.right < 819:
            self.player.new_animation = "down-run"
            self.player.vector.x = 1
            self.player.vector.y = 0
        else:
            self.player.new_animation = "idle"
            self.player.vector.x = 0
            self.player.vector.y = 0
        
        if debug:
            if keys[pygame.K_p]:
                print(self.player.rect.x, self.player.rect.y)
            if keys[pygame.K_o]:
                print(self.bullet_group)
            if keys[pygame.K_i]:
                print(self.enemy_group)
            if keys[pygame.K_r]:
                self.generate_enemy_line()
                self.enemy_spawn_cooldown = MAX_ENEMY_SPAWN_COOLDOWN
        
        # Se è premuto il tasto spazio e il cooldown per la 
        # ricarica dei proiettili è 0 allora crea un oggetto
        # proiettile e aggiungilo al "Group" con tutti i proiettili
        if (keys[pygame.K_z] or keys[pygame.K_k]) and self.shuriken_cooldown == 0:
            shuriken = Bullet(
                BULLETS_SPRITES['shuriken'],
                self.player.rect.center[0], 
                self.player.rect.center[1],
                True,
                False)
            self.shuriken_cooldown = MAX_SHURIKEN_COOLDOWN
            self.bullet_group.add(shuriken)
            self.game_points['score'] += SHURIKEN_POINTS
            self.game_points['shuriken_shooted'] += 1
        elif (keys[pygame.K_x] or keys[pygame.K_l]) and self.kunai_cooldown == 0:
            kunai = Bullet(
                BULLETS_SPRITES["kunai"],
                self.player.rect.center[0], 
                self.player.rect.center[1],
                False,
                False)
            self.kunai_cooldown = MAX_KUNAI_COOLDOWN
            self.bullet_group.add(kunai)
            self.game_points['score'] += KUNAI_POINTS
            self.game_points['kunai_shooted'] += 1
                    
    def generate_enemy_line(self):
        self.enemy_group.empty()
        for i in range(6):
            self.enemy_group.add(Block('blue', 60, 60, (60 + 130 * i, 550), self.enemy_speed))
    
    def main_loop(self):
        while self.run:
            for event in pygame.event.get():
    
                # Se l'evento è di tipo QUIT o se è di tipo 
                # tasto ed il tasto premuto è q allora esce 
                # dal gioco
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.run = False
        
            # 30 volte in un secondo
            self.clock.tick(30)
        
            # Cancella tutto e ridisegna gli oggetti presenti 
            # sullo schermo di gioco
            self.screen.fill("white")
            
            #Diminuisci il cooldown per lanciare i proiettiliù
            if self.increase_speed_cooldwn > 0:
                self.increase_speed_cooldwn -= 1
            else:
                self.enemy_speed += 1
                self.increase_speed_cooldwn = MAX_INCREASE_SPEED_COOLDOWN
                if self.enemy_speed > 3:
                    self.player.speed =  3 + self.enemy_speed
                print(self.player.speed)

            if self.shuriken_cooldown > 0:
                self.shuriken_cooldown -= 1
        
            if self.kunai_cooldown > 0:
                self.kunai_cooldown -= 1
            
            if self.invulnerability_cooldown > 0:
                self.invulnerability_cooldown -=1
            
            if self.enemy_spawn_cooldown > 0:
                self.enemy_spawn_cooldown -=1
            else:
                if enemy_spawn:
                    self.enemy_spawn_cooldown = MAX_ENEMY_SPAWN_COOLDOWN
                    self.enemy_group.add(Block('blue', 60, 60, (randint(30, 770), 650), self.enemy_speed))                
            
            #Aggiorna tutti gli elementi di gioco
            self.get_input()
            self.player.update()
            self.check_enemies()
            self.check_bullets()
            
            for bullet in self.bullet_group:
                bullet.update()

            for enemy in self.enemy_group:
                enemy.update()
            
            self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
            self.bullet_group.draw(self.screen)
            self.enemy_group.draw(self.screen)

            pygame.display.flip()
            if self.life == 0 or self.enemy_passed > 10:
                print(f"Hai perso!\nIl tuo punteggio: {self.game_points}\nSpeed: {self.enemy_speed}, {self.player.speed}")
                self.run = False
        pygame.quit()


if __name__ == "__main__":
    enemy_spawn = [True, False][0]
    enemy_moving = [True, False][0]
    debug = [True, False][0]
    game = Game()
    game.main_loop()
