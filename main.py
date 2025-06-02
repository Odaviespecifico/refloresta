from game import Game
from menu import tela_inicial


if __name__ == '__main__':
    global som
    g = Game()
    while True:
        tela_inicial()
        g.playing = True
        g.game_loop()