from PPlayTeste.gameimage import *
from PPlayTeste.sound import *
# from game import Game

class Player:
    fire_list = []
    def __init__(self, game):
        self.game = game
        self.spaceship = GameImage("graphic/player.png")
        self.spaceship.x, self.spaceship.y = 300 - self.spaceship.width/2, 600 - self.spaceship.height
        self.vLaser = 200
        self.vPlayer = 400
        self.ready = 0
        self.laser_sound = Sound("sounds/nao.ogg")

    def check_events(self):
        
        if self.game.keyboard.key_pressed("LEFT"):
            if self.spaceship.x < -60:
                self.spaceship.x = 600
            self.spaceship.x -= self.vPlayer * self.game.screen.delta_time()

        if self.game.keyboard.key_pressed("RIGHT"):
            if self.spaceship.x > 600:
                self.spaceship.x = -60
            self.spaceship.x += self.vPlayer * self.game.screen.delta_time()

        # Define o tempo de recarga
        if self.game.difficulty == 1:
            self.cooldown = 0.1
        if self.game.difficulty == 2:
            self.cooldown = 1.0
        if self.game.difficulty == 3:
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
            # print(fire.x, fire.y)
            fire.draw()
        
    def reset(self):
        Player.fire_list = []
        self.spaceship.x, self.spaceship.y = 300 - self.spaceship.width/2, 600 - self.spaceship.height
        Player(self.game)