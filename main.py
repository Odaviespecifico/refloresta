from game import Game
from menu import tela_inicial


if __name__ == '__main__':
    tela_inicial()  # Mostra o menu
    g = Game()
    g.playing = True
    g.game_loop()