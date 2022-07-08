from PPlay.gameimage import *
from PPlay.sound import *
from PPlay.sprite import *

class Player:
    fire_list = []
    def __init__(self, game):
        self.game = game
        self.spaceship = Sprite("graphic/player.png",5)
        self.spaceship.x, self.spaceship.y = 300 - self.spaceship.width/2, 600 - self.spaceship.height
        self.vLaser = 200
        self.vPlayer = 400
        self.ready = 0
        self.shield_cooldown, self.tempo = 3, 0
        self.shield = False
        self.laser_sound = Sound("sounds/nao.ogg")

    def check_events(self):
        if self.shield:
            self.tempo += self.game.screen.delta_time()
            if self.tempo >= self.shield_cooldown:
                self.tempo = 0
                self.shield = False
            
        if self.game.keyboard.key_pressed("LEFT"):
            if self.spaceship.x < -60:
                self.spaceship.x = 600
            self.spaceship.x -= self.vPlayer * self.game.screen.delta_time()

        if self.game.keyboard.key_pressed("RIGHT"):
            if self.spaceship.x > 600:
                self.spaceship.x = -60
            self.spaceship.x += self.vPlayer * self.game.screen.delta_time()

        # Define o tempo de recarga
        if 2.0 > self.game.difficulty >= 1.0:
            self.cooldown = 0.3
        if 3.0 > self.game.difficulty >= 2.0:
            self.cooldown = 1.0
        if self.game.difficulty >= 3.0:
            self.cooldown = 1.2
        self.ready += self.game.screen.delta_time()
        
        # Atira de acordo com a dificuldade
        if self.game.keyboard.key_pressed("SPACE"):
            if self.ready >= self.cooldown:
                laser = GameImage("graphic/laser.png")
                laser.x, laser.y = self.spaceship.x + self.spaceship.width/2, self.spaceship.y
                Player.fire_list.append(laser)
                self.ready = 0
                self.laser_sound.play()
        # Remove o tiro se chegar no inicio da janela
        if len(Player.fire_list) >= 1:
            if Player.fire_list[0].y <= 0:
                Player.fire_list.pop(0)
            
        

    def draw_laser(self):
        for fire in Player.fire_list:
            fire.y -= self.vLaser * self.game.screen.delta_time()
            fire.draw()
        
    def reset(self):
        Player.fire_list = []
        self.spaceship.x, self.spaceship.y = 300 - self.spaceship.width/2, 600 - self.spaceship.height
        self.shield = False
        Player(self.game)