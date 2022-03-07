from random import randint, choice
from os import getcwd
import pygame
pygame.font.init()

from Classes.bullet import Bullet
from Classes.player import Player
from Classes.utils import import_bullets, import_buttons
from Classes.mouse_pad import MousePad

SCREEN_SIZE = [(800, 450), (1152, 648), (1280, 720), (1536, 864)][2]#(800, 600)
SCREEN_CENTER = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
MAX_SHURIKEN_COOLDOWN = 60
MAX_KUNAI_COOLDOWN = 120
MAX_INVULNERABILITY_COOLDOWN = 120
MAX_ENEMY_SPAWN_COOLDOWN = 60
MAX_INCREASE_SPEED_COOLDOWN = 600
BULLETS_SPRITES = import_bullets("images/bullets/",64,64)
BULLET_SPEED = 5
ENEMY_HIT_POINTS = 100
KUNAI_POINTS = 10
SHURIKEN_POINTS = 10
SCORE_FONT = pygame.font.Font("EightBitDragon-anqx.ttf", SCREEN_SIZE[0]//25)
GAME_FOLDER = getcwd()
HEART_CONTAINER = pygame.transform.scale(pygame.image.load(f'{GAME_FOLDER}/images/heart_container.png'), (100, 100))
BRICK = pygame.transform.scale(pygame.image.load(f'{GAME_FOLDER}/images/brick.png'), (40, 40))
ENEMY_COUNTER = pygame.Surface((SCREEN_SIZE[0]//20, SCREEN_SIZE[0]//20))
ENEMY_COUNTER.fill('blue')
GAME_OVER_IMAGE = pygame.image.load(f'{GAME_FOLDER}/images/game-over.png')
GAME_OVER_FONT = pygame.font.Font("EightBitDragon-anqx.ttf", 100)
ENEMY_IMAGE = [pygame.transform.scale(pygame.image.load(f'{GAME_FOLDER}/images/enemies/{enemy}.png'), (SCREEN_SIZE[0]//10, SCREEN_SIZE[0]//10)) for enemy in ["green_snake", "purple_snake"]]
BUTTON_IMAGE = import_buttons("/images/buttons/")

class Button(pygame.sprite.Sprite):
    def __init__(self, button_name: str, phase: str, posy: int, dimension: tuple):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.transform.scale(BUTTON_IMAGE[button_name], dimension)
       self.rect = self.image.get_rect()
       self.rect.center = (SCREEN_SIZE[0]//2, posy)
       self.phase = phase

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.Surface, pos: tuple, speed: int):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(center= pos)
        self.speed = speed
        self.animation_speed = 0.3
        self.counter = 0
    
    def update(self):
        if enemy_moving:
            self.rect.y -= self.speed

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class Game:
    def __init__(self):
        if full_screen:
            self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN) 
            #self.screen = pygame.display.set_mode((SCREEN_SIZE), SCALED + NOFRAME + FULLSCREEN, 32, vsync=1)
        else:
            self.screen = pygame.display.set_mode((SCREEN_SIZE)) 
        self.clock = pygame.time.Clock()
        self.player = Player(SCREEN_CENTER)
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        self.run = True
        self.restart = False
        self.shuriken_cooldown = 0
        self.kunai_cooldown = 0
        self.mouse = MousePad(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        self.invulnerability_cooldown = MAX_INVULNERABILITY_COOLDOWN
        self.enemy_spawn_cooldown = 20
        self.increase_speed_cooldwn = MAX_INCREASE_SPEED_COOLDOWN
        self.life = 3
        self.phase = "game"
        self.enemy_speed = 0.5
        self.enemy_passed = 0
        self.game_points = {
            "score" : 0,
            "enemy_killed" : 0,
            "shuriken_shooted" : 0,
            "kunai_shooted" : 0
        }

    def check_bullets(self):
        for bullet in self.bullet_group:
            typo = "shuriken" if bullet.is_rotating else "kunai"
            if bullet.rect.top > SCREEN_SIZE[1] or bullet.rect.bottom < 0 or bullet.rect.left > SCREEN_SIZE[0] or bullet.rect.right < 0:
                self.bullet_group.remove(bullet)

            for enemy in self.enemy_group:
                if bullet.is_collided_with(enemy):
                    self.enemy_group.remove(enemy)
                    self.game_points['score'] += ENEMY_HIT_POINTS
                    self.game_points['enemy_killed'] += 1
                    if bullet.destroy_at_collision:
                        self.bullet_group.remove(bullet)
    
    def check_enemies(self):
        for enemy in self.enemy_group:
            if enemy.rect.bottom < -10:
                self.enemy_passed += 1
                self.enemy_group.remove(enemy)
            if enemy.is_collided_with(self.player) and self.invulnerability_cooldown == 0:
                self.life -=1
                self.invulnerability_cooldown = MAX_INVULNERABILITY_COOLDOWN
    
    def get_game_input(self):
        # Trovo i tasti che sono stati premuti facendo
        # muovere il personaggio nella direzione scelta 
        # scegliendo il tipo di animazione durante la camminata
        if (self.keys[pygame.K_UP] or self.keys[pygame.K_w]) and self.player.rect.top > 0:
            self.player.new_animation = "down-run"
            self.player.vector.x = 0
            self.player.vector.y = -1
        elif (self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]) and self.player.rect.bottom < SCREEN_SIZE[1]:
            self.player.new_animation = "down-run"
            self.player.vector.x = 0
            self.player.vector.y = 1
        elif (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]) and self.player.rect.left > -19:
            self.player.new_animation = "down-run"
            self.player.vector.x = -1
            self.player.vector.y = 0
        elif (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]) and self.player.rect.right < SCREEN_SIZE[0]:
            self.player.new_animation = "down-run"
            self.player.vector.x = 1
            self.player.vector.y = 0
        else:
            self.player.new_animation = "idle"
            self.player.vector.x = 0
            self.player.vector.y = 0
        
        if debug:
            if self.keys[pygame.K_u]:
                self.generate_enemy_line()
                self.enemy_spawn_cooldown = MAX_ENEMY_SPAWN_COOLDOWN
            if self.keys[pygame.K_y]:
                self.life = 0
                self.enemy_passed = 10
        
        # Se è premuto il tasto spazio e il cooldown per la 
        # ricarica dei proiettili è 0 allora crea un oggetto
        # proiettile e aggiungilo al "Group" con tutti i proiettili
        if (self.keys[pygame.K_z] or self.keys[pygame.K_k]) and self.shuriken_cooldown == 0:
            shuriken = Bullet(
                BULLETS_SPRITES['shuriken'],
                self.player.rect.center[0] + 0, 
                self.player.rect.center[1],
                True,
                False)
            self.shuriken_cooldown = MAX_SHURIKEN_COOLDOWN
            self.bullet_group.add(shuriken)
            self.game_points['score'] += SHURIKEN_POINTS
            self.game_points['shuriken_shooted'] += 1
        elif ((self.keys[pygame.K_x] or self.keys[pygame.K_l]) and self.kunai_cooldown == 0):
            kunai1 = Bullet(
                BULLETS_SPRITES["kunai"],
                self.player.rect.left, 
                self.player.rect.center[1] + 20,
                False,
                False,
                "left")
            kunai2 = Bullet(
                BULLETS_SPRITES['kunai'],
                self.player.rect.right - 0, 
                self.player.rect.center[1] + 20,
                False,
                False,
                "right")
            
            self.kunai_cooldown = MAX_KUNAI_COOLDOWN
            self.bullet_group.add(kunai1)
            self.bullet_group.add(kunai2)
            self.game_points['score'] += KUNAI_POINTS
            self.game_points['kunai_shooted'] += 2 
            
                    
    def generate_enemy_line(self):
        self.enemy_group.empty()
        for i in range(6):
            self.enemy_group.add(Enemy(choice(ENEMY_IMAGE), (randint(30, 770), 650), self.enemy_speed))
    
    def draw_bricks(self):
        for x in range(0, SCREEN_SIZE[0] + 1, 40):
            for y in range(0, SCREEN_SIZE[1] + 1, 40):
                self.screen.blit(BRICK, (x, y))

    def game_over(self):
        self.screen.blit(GAME_OVER_IMAGE, (0, 0))
        score = self.game_points['score']
        
        self.button_group.add(Button("restart-1", "game", 350, (1080//2, 458//2)))
        self.button_group.draw(self.screen)
            
        text = GAME_OVER_FONT.render(f'Score: {score}', 1, (0,0,0))
        pos = text.get_rect(center=(SCREEN_SIZE[0]//2,  100))
        self.screen.blit(text, pos)
        
        if self.mouse.left_pressed:
            self.phase = self.mouse.is_colliding_with_group(self.button_group)
        
        if self.phase in ["game", "main_menu"]:
            self.reset_game()
        else:
            self.phase = "game_over"
    
    def pause_game(self):
        self.screen.blit(GAME_OVER_IMAGE, (0, 0))
        self.button_group.add(Button("start-1", "game", 300, (1080//2, 458//2)))
        self.button_group.draw(self.screen)
        
        if self.mouse.left_pressed:
            self.phase = self.mouse.is_colliding_with_group(self.button_group)
        
        if self.phase in ["game", "main_menu"]:
            pass
        else:
            self.phase = "pause"
           
    def reset_game(self):
        self.enemy_group.empty()
        self.bullet_group.empty()
        self.shuriken_cooldown = 0
        self.kunai_cooldown = 0
        self.enemy_spawn_cooldown = 10
        self.life = 3
        self.enemy_speed = 1
        self.enemy_passed = 0
        self.player = Player(SCREEN_CENTER)
        self.game_points = {
            "score" : 0,
            "enemy_killed" : 0,
            "shuriken_shooted" : 0,
            "kunai_shooted" : 0
        }

    def game_loop(self):
        self.draw_bricks()
        #Diminuisci il cooldown per lanciare i proiettiliù
        if self.increase_speed_cooldwn > 0:
            self.increase_speed_cooldwn -= 1
        else:
            self.enemy_speed += 0.5
            self.increase_speed_cooldwn = MAX_INCREASE_SPEED_COOLDOWN
            if self.enemy_speed > 3:
               self.player.speed =  1.5 + self.enemy_speed

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
                self.enemy_group.add(Enemy(choice(ENEMY_IMAGE), (randint(30, SCREEN_SIZE[0]-30), SCREEN_SIZE[1] + 50), self.enemy_speed))                
            
        #Aggiorna tutti gli elementi di gioco
        self.get_game_input()
        self.player.update()
        self.check_enemies()
        self.check_bullets()
        
        for bullet in self.bullet_group:
            bullet.update()

        for enemy in self.enemy_group:
            enemy.update()
            
        #Disegno gli elementi dell'interfaccia
        for i in range(self.life):
            self.screen.blit(HEART_CONTAINER, ((SCREEN_SIZE[0]//15)*i+SCREEN_SIZE[0]//40, 5))
        
        self.screen.blit(ENEMY_COUNTER, (SCREEN_SIZE[0]//2.5-ENEMY_COUNTER.get_size()[0]-SCREEN_SIZE[0]//60, SCREEN_SIZE[1]//50))
        counter= SCORE_FONT.render(f'X{self.enemy_passed}', 1, (0,0,0))
        self.screen.blit(counter, (SCREEN_SIZE[0]//2.5, SCREEN_SIZE[1]//40)) 
            
        text = SCORE_FONT.render(str(self.game_points['score']), 1, (0,0,0))
        self.screen.blit(text, (SCREEN_SIZE[0]-SCREEN_SIZE[0]//7, SCREEN_SIZE[1]/50))
             
        #Disegno il personaggio, i proiettili e i nemici
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        if self.life == 0 or self.enemy_passed > 10:
            self.phase = "game_over"
        
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
                    if event.key == pygame.K_r and self.phase == "game_over":
                        self.phase = "game"
                        self.reset_game()
                    if event.key == pygame.K_p:
                        self.phase = "pause" if self.phase == "game" else "game"
        
            # 30 volte in un secondo
            self.clock.tick(60)
            # Cancella tutto e ridisegna gli oggetti presenti 
            # sullo schermo di gioco
            self.mouse.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
            self.keys = pygame.key.get_pressed()
            self.screen.fill("white")
            if self.phase == "game":
                self.game_loop()
            elif self.phase == "pause":
                self.pause_game()
            elif self.phase == "game_over":
                self.game_over()
            pygame.display.flip()
            
        pygame.quit()


if __name__ == "__main__":
    full_screen = [True, False][0]
    enemy_spawn = [True, False][0]
    enemy_moving = [True, False][0]
    debug = [True, False][0]
    game = Game()
    game.main_loop()
    print("Banana ")
