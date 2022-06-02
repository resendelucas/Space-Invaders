from menu import Menu
from game import Game
from alien import Alien
from player import Player
from rank import Rank
from PPlayTeste.gameimage import *

game = Game()
player = Player(game)
alien = Alien(game,player)
rank = Rank(game, game.player_name, game.score)
menu = Menu(game, player, alien, rank)

while True:
    game.background.draw()
    if menu.rank_menu:
        game.screen.set_background_color((100,100,100))
    menu.check_events()
    menu.draw_buttons()
    # game.check_events()
    if game.playing:
        game.screen.set_background_color((100,100,100))
        game.screen.draw_text((f"Score: {game.score}"), 10, -10, size=18, color=(255,255,255), font_name="font/Pixeled.ttf")
        game.screen.draw_text((f"Life: {game.player_life}"), 500, -10, size=18, color=(255,255,255), font_name="font/Pixeled.ttf")
        
        if not game.game_over:
            player.check_events()
            alien.check_alien()
            alien.shoot()
            game.check_events()
            player.draw_laser()
        alien.draw_aliens()
        player.spaceship.draw()

        if game.game_over:
            game.game_over_screen.draw()
            game.screen.draw_text((f"NOME: "), 200,250, size=18, color=(255,255,255), font_name="font/Pixeled.ttf")
            game.write()
            game.screen.draw_text((f"{game.player_name}"), 300, 250, size=18, color=(255,255,255), font_name="font/Pixeled.ttf")
            game.screen.draw_text((f"SCORE: {game.score}"), 200, 300, size=18, color=(255,255,255), font_name="font/Pixeled.ttf")
    game.screen.update()
