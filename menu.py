from PPlayTeste.gameimage import *
from PPlayTeste.window import *

class Menu:
    def __init__(self, game, player, alien, rank):
        self.game = game
        self.screen = game.screen
        self.player = player
        self.alien = alien
        self.rank = rank
        self.mouse = self.screen.get_mouse()
        self.keyboard = self.screen.get_keyboard()
        self.click = False
        self.click_cooldown = 0.4
        self.main_menu, self.dif_menu, self.rank_menu = True, False, False

        self.buttons_list = [GameImage(f"botao/jogar1.png"), GameImage(f"botao/dificuldade1.png"), 
        GameImage(f"botao/ranking1.png"), GameImage(f"botao/sair1.png"), GameImage(f"botao/facil1.png"), 
        GameImage(f"botao/medio1.png"), GameImage(f"botao/dificil1.png")]
        self.buttons_list_over = [GameImage(f"botao/jogar2.png"), GameImage(f"botao/dificuldade2.png"), 
        GameImage(f"botao/ranking2.png"), GameImage(f"botao/sair2.png"), GameImage(f"botao/facil2.png"), 
        GameImage(f"botao/medio2.png"), GameImage(f"botao/dificil2.png")]
        self.get_buttons(self.buttons_list)
        self.get_buttons(self.buttons_list_over)

    def get_buttons(self, lista):
        first = 200
        for i in range(7):
            if i == 4:
                first = 300
            lista[i].x, lista[i].y = (self.screen.width/2 - lista[i].width/2), first
            first += 100

    def draw_buttons(self):
        if self.main_menu:
            self.buttons_list[0].draw()
            self.buttons_list[1].draw()
            self.buttons_list[2].draw()
            self.buttons_list[3].draw()

            if self.mouse.is_over_object(self.buttons_list[0]):
                self.buttons_list_over[0].draw()
            if self.mouse.is_over_object(self.buttons_list[1]):
                self.buttons_list_over[1].draw()
            if self.mouse.is_over_object(self.buttons_list[2]):
                self.buttons_list_over[2].draw()
            if self.mouse.is_over_object(self.buttons_list[3]):
                self.buttons_list_over[3].draw()
                
        if self.dif_menu:
            self.buttons_list[4].draw()
            self.buttons_list[5].draw()
            self.buttons_list[6].draw()

            if self.mouse.is_over_object(self.buttons_list[4]) or self.game.difficulty == 1:
                self.buttons_list_over[4].draw()
            if self.mouse.is_over_object(self.buttons_list[5]) or self.game.difficulty == 2:
                self.buttons_list_over[5].draw()
            if self.mouse.is_over_object(self.buttons_list[6]) or self.game.difficulty == 3:
                self.buttons_list_over[6].draw()
        
        if self.rank_menu:
            self.rank.draw_rank()
          
    def check_click(self):
        if self.click_cooldown < 0.2:
            self.click_cooldown += self.game.screen.delta_time()
        if self.mouse.is_button_pressed(1) and self.click_cooldown >= 0.2:
            self.click_cooldown = 0
            return True
        return False

    def check_events(self):
        if self.mouse.is_over_object(self.buttons_list[0]) and self.check_click() and self.main_menu:
                self.game.playing = True
                self.main_menu = False
                self.dif_menu = False
                self.game.play_music()

        if self.mouse.is_over_object(self.buttons_list[1]) and self.check_click():
                self.dif_menu = True
                self.main_menu = False
        
        if self.mouse.is_over_object(self.buttons_list[2]) and self.check_click() and self.main_menu:
                self.dif_menu = False
                self.main_menu = False
                self.rank_menu = True
    
        if self.mouse.is_over_object(self.buttons_list[3]) and self.main_menu and self.check_click():
                self.screen.close()

        if self.keyboard.key_pressed("ESC"):
            if not self.main_menu:
                self.game.playing = False
                self.dif_menu = False
                self.main_menu = True
                self.rank_menu = False
                self.game.stop_music()
                self.alien.reset()
                self.player.reset()
                self.game.reset()

        if self.game.playing and self.game.game_over:
            if self.game.leave_game:
                self.game.playing = False
                self.dif_menu = False
                self.main_menu = True
                self.game.stop_music()
                self.alien.reset()
                self.player.reset()
                self.game.reset()

        if not self.game.playing and self.dif_menu and self.check_click():
            if self.mouse.is_over_object(self.buttons_list[4]):
                self.game.difficulty = 1
            if self.mouse.is_over_object(self.buttons_list[5]):
                self.game.difficulty = 2
            if self.mouse.is_over_object(self.buttons_list[6]):
                self.game.difficulty = 3