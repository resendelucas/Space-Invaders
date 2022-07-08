from PPlay.gameimage import *
from PPlay.sound import *
from random import choice, randint

lins = 4
col = 9
class Alien():

    alien_list = [[0 for _ in range(col)] for _ in range(lins)]
    alien_fire = []
    boss_index = [0,0]
    boss_life = 3
    def __init__(self,game,player):
        self.game = game
        self.player = player
        self.cooldown, self.ready = 2, 0
        self.vLaser = 100
        self.vAlien = 50
        self.direction = 1
        self.hit_sound = Sound("sounds/calma.ogg")
        self.hit_sound.decrease_volume(10)
        self.get_aliens()
        
    def get_aliens(self):
        random_boss_line = randint(0,lins-1)
        random_boss = randint(0, len(Alien.alien_list[random_boss_line])-1)
        self.boss_index[0] = random_boss_line
        self.boss_index[1] = random_boss
        Alien.alien_list[random_boss_line][random_boss] = 1
        change_y = 50
        for i in range(lins):
            if i == 0: dir = 'green'
            if 1 <= i <= 2: dir = 'yellow'
            if i >= 3: dir = 'red'
            change_x = 80
            for j in range(col):
                alien_image = GameImage(f"graphic/{dir}.png")
                if Alien.alien_list[i][j] == 1:
                    alien_image = GameImage(f"graphic/boss.png")
                Alien.alien_list[i][j] = alien_image
                Alien.alien_list[i][j].x = change_x 
                Alien.alien_list[i][j].y = change_y
                change_x += alien_image.width + 10
            change_y += 50

    def check_alien(self):
        for lin in Alien.alien_list:
            for alien in lin:
                if alien != 0:
                    alien.x += (self.vAlien + self.game.add_vel) * self.game.difficulty * self.game.screen.delta_time() * self.direction

                    if alien.x >= self.game.screen.width - alien.width:
                        alien.x = self.game.screen.width - alien.width - 1
                        self.move_down()
                        self.direction *= -1

                    if alien.x <= 0:
                        alien.x = 1
                        self.move_down()
                        self.direction *= -1
                        
                    if alien.y >= self.game.screen.height:
                        self.game.gameover = True
                    
        if Alien.alien_list == [[],[],[],[]]:
            self.game.new_round += 1
            self.game.add_vel = 0
            Alien.alien_list = [[0 for _ in range(col)] for _ in range(lins)]
            self.game.difficulty += 0.25
            Alien.alien_fire = []
            Alien.boss_life = 3
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
                    Alien.alien_fire.pop(0)
                    if not self.player.shield:
                        self.hit_sound.play()
                        self.game.player_life -= 1
                        self.player.spaceship.x, self.player.spaceship.y = 300 - self.player.spaceship.width/2, 600 - self.player.spaceship.height
                        self.player.shield = True
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
        self.boss_life = 3
        Alien(self.game, self.player)
