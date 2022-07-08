from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sound import *
from alien import Alien
from player import Player
from random import randint
from rank import Rank

class Game:
    player_name = ''
    def __init__(self):
        self.screen = Window(600,600)
        self.playing = False
        self.game_over, self.leave_game = False, False
        self.difficulty = 1
        self.score = 0
        self.add_vel, self.new_round = 0, 0
        self.player_life = 3
        self.tempo, self.game_loop = 0, 0
        self.last_fps = 0
        self.player = Player(self)
        self.alien = Alien(self, self.player)
        self.keyboard = self.screen.get_keyboard()
        self.background = GameImage("botao/space.jpg")
        self.game_over_screen = GameImage("graphic/gameOver.jpg")
        self.game_over_screen.x, self.game_over_screen.y = self.screen.width/2 - self.game_over_screen.width/2, self.screen.height/2 - self.game_over_screen.height/2
        self.game_song = Sound("sounds/invaders-song2.wav")
        self.sound_list = [Sound("sounds/ai.ogg"),Sound("sounds/ui.ogg"),Sound("sounds/tome.ogg"),
        Sound("sounds/chega.ogg"),Sound("sounds/tapa.ogg"),Sound("sounds/tudo.ogg")]
        for sound in self.sound_list:
            sound.decrease_volume(10)
        self.screen.set_title("Space Invaders")

    def check_events(self):
        # Pegando colisão de baixo para cima:
        for shot in Player.fire_list:
            for lin in range(len(Alien.alien_list) -1, -1, -1):
                for col, alien in enumerate(Alien.alien_list[lin]):
                    if alien.y >= self.screen.height:
                        self.game_over = True
                    if len(Player.fire_list) >= 1:
                        if shot.collided(alien):
                            # verifica se acertou o boss
                            if lin == Alien.boss_index[0]:
                                if col != Alien.boss_index[1]:
                                    if col < Alien.boss_index[1]:
                                        Alien.boss_index[1] -= 1
                                    Alien.alien_list[lin].remove(alien)
                                    if lin == 0: self.score += 300
                                    if 1 <= lin <= 2: self.score += 200
                                    if lin == 3: self.score += 100

                                elif col == Alien.boss_index[1]:
                                    if Alien.boss_life == 1:
                                        Alien.alien_list[lin].remove(alien)
                                        self.score += 1000
                                    else:
                                        Alien.boss_life -= 1
                            else:
                                Alien.alien_list[lin].remove(alien)
                                if lin == 0: self.score += 300
                                if 1 <= lin <= 2: self.score += 200
                                if lin == 3: self.score += 100
                            if self.new_round >= 1:
                                self.add_vel += 5
                            Player.fire_list.remove(shot)
                            self.fire_random()
                            
                            


            for shot_alien in Alien.alien_fire:
                if shot.collided(shot_alien):
                    Player.fire_list.remove(shot)
                    Alien.alien_fire.remove(shot_alien)
        if self.player_life <= 0 or self.keyboard.key_pressed("g"):
            self.game_over = True

    def fire_random(self):
        self.sound_list[randint(0,len(self.sound_list)-1)].play()

    def play_music(self):
        if not self.game_song.is_playing():
            self.game_song.set_repeat(True)
            self.game_song.play()

    def stop_music(self):
        if self.game_song.is_playing():
            self.game_song.stop()
    

    def write(self):
        a = self.keyboard.show_key_pressed()
        if a != None and a != 27 and a != 13:
            if a == 8:
                Game.player_name = Game.player_name[:len(Game.player_name)-1]
            else:
                try:
                    Game.player_name += chr(a)
                except ValueError:
                    print("invalido")
        if self.keyboard.key_pressed("ENTER"):
                Rank(self, self.player_name, self.score).update_rank()
                self.leave_game = True

    def show_fps(self):
        self.tempo += self.screen.delta_time()
        self.game_loop += 1
        if self.tempo >= 1:
            self.last_fps = self.game_loop
            self.tempo = 0
            self.game_loop = 0
        self.screen.draw_text((f"{self.last_fps}"), 300, -10, size=18, color=(205,255,255), font_name="font/Pixeled.ttf")

    def reset(self):
        self.player_life = 3
        self.score = 0
        self.game_over,self.leave_game = False, False
        Game.player_name = ''