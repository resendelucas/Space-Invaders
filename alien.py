from PPlayTeste.gameimage import *
from PPlayTeste.sound import *
from random import choice

lins = 4
col = 9
class Alien():
    alien_list = [[0 for _ in range(col)] for _ in range(lins)]
    alien_fire = []
    def __init__(self,game,player):
        self.game = game
        self.player = player
        self.vAlien = 50
        self.direction = 1
        self.cooldown = 2
        self.vLaser = 100
        self.ready = 0
        self.new_round = False
        self.hit_sound = Sound("sounds/calma.ogg")
        self.hit_sound.decrease_volume(40)
        self.get_aliens()
        
    def get_aliens(self):
        change_y = 50
        for i in range(lins):
            if i == 0: dir = 'green'
            if 1 <= i <= 2: dir = 'yellow'
            if i >= 3: dir = 'red'
            change_x = 80
            for j in range(col):
                self.image = GameImage(f"graphic/{dir}.png")
                Alien.alien_list[i][j] = self.image
                Alien.alien_list[i][j].x = change_x 
                Alien.alien_list[i][j].y = change_y
                change_x += self.image.width + 10
            change_y += 50

    def check_alien(self):
        for lin in range(len(Alien.alien_list)):
            for alien in Alien.alien_list[lin]:
                alien.x += self.vAlien * self.game.difficulty * self.game.screen.delta_time()
                if alien.x >= self.game.screen.width - alien.width:
                    alien.x = self.game.screen.width - alien.width - 1
                    self.move_down()
                    self.vAlien *= -1
                if alien.x <= 0:
                    alien.x = 1
                    self.move_down()
                    self.vAlien *= -1
                if alien.y >= self.game.screen.height:
                    self.game.gameover = True
                    
        if Alien.alien_list == [[],[],[],[]]:
            Alien.alien_list = [[0 for _ in range(col)] for _ in range(lins)]
            self.get_aliens()

    def shoot(self):
        if self.ready < self.cooldown:
            self.ready += self.game.screen.delta_time()
        if self.ready >= self.cooldown:
            if len(Alien.alien_list) >= 1:
                random_alien = choice(Alien.alien_list)
                if random_alien != []:
                    alien = choice(random_alien)
                    laser = GameImage("graphic/alien-laser.png")
                    laser.x, laser.y = alien.x + alien.width/2, alien.y + alien.height
                    Alien.alien_fire.append(laser)
                    self.ready = 0
        
        if len(Alien.alien_fire) >= 1:
                if Alien.alien_fire[0].y >= self.game.screen.height:
                    Alien.alien_fire.pop(0)


        for fire in Alien.alien_fire:
            fire.y += self.vLaser * self.game.screen.delta_time()
            fire.draw()
        
        if Alien.alien_fire != []:
            for alien_shot in Alien.alien_fire:
                if alien_shot.collided(self.player.spaceship):
                    self.hit_sound.play()
                    self.game.player_life -= 1
                    Alien.alien_fire.pop(0)

    def draw_aliens(self):
        for lin in range(len(Alien.alien_list)):
            for alien in Alien.alien_list[lin]:
                alien.draw()

    def move_down(self):
        for lin in range(len(Alien.alien_list)):
            for alien in Alien.alien_list[lin]:
                alien.y = alien.y + 15

    def reset(self):
        Alien.alien_list = [[0 for _ in range(col)] for _ in range(lins)]
        Alien.alien_fire = []
        Alien(self.game, self.player)
