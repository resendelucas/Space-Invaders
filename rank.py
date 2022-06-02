class Rank():
    def __init__(self, game, name, score):
        self.game = game
        self.name = name
        self.score = score

    def update_rank(self):
        if self.score != 0:
            with open("ranking.txt",'r+',encoding = 'utf-8') as f:
                # f.write(f"{self.name}#{self.score}\n")
                content = f.read()
                if content == '':
                    f.write(f"{self.name}#{self.score}")
                    print("aqui")
                else:
                    f.write(f"{self.name}#{self.score}")
                    f.write('\n')

    def key_ord(self, line):
        line_list = line.strip().split('#')
        score = int(line_list[1])
        return score
  
    def sort_rank(self):
        with open('ranking.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines.sort(key=self.key_ord, reverse=True)
            with open('ranking-ordenado.txt', 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line)

    def draw_rank(self):
        self.sort_rank()
        pos_y = 100
        self.game.screen.draw_text((f"PLAYER"), 50, 10, size=32, color=(255,255,255), font_name="font/Pixeled.ttf")
        self.game.screen.draw_text((f"SCORE"), 400, 10, size=32, color=(255,255,255), font_name="font/Pixeled.ttf")
        with open("ranking-ordenado.txt",'r',encoding = 'utf-8') as f:
            lines = f.readlines()
            for line in lines:
                player, player_score = line.split('#')[0], int(line.split('#')[1])
                self.game.screen.draw_text((f"{player}"), 50, pos_y, size=32, color=(255,255,255), font_name="font/Pixeled.ttf")
                self.game.screen.draw_text((f"{player_score}"), 435, pos_y, size=32, color=(255,255,255), font_name="font/Pixeled.ttf")
                pos_y += 50