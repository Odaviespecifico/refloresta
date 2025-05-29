import pygame
from menu import *
from Entities import Player, Trash, Arvores
from utils import Background, TileMap

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY = self.DOWN_KEY = self.START_KEY = self.BACK_KEY = False
        self.SPACE_KEY = self.E_Key = self.Q_Key = False
        self.scale = 60
        self.DISPLAY_W, self.DISPLAY_H = 16*self.scale, 9*self.scale
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        # self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)),flags=pygame.FULLSCREEN|pygame.SCALED)
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.curr_menu = None
        #self.main_menu = MainMenu(self)
        #self.options = OptionsMenu(self)
        #self.credits = CreditsMenu(self)
        #self.curr_menu = self.main_menu
        self.background = Background(5)
        self.jogador = Player()
        self.map = TileMap('assets\maps\map_test.csv')
        self.trash = Trash(self.map.toprectlist)
        self.pontuação = 0
        self.fullscreen = False
        self.Arvores = Arvores()
        self.music_playing = False
        self.mapa = 0
        self.treecounter = 0
        pygame.mixer.init() #inicia música
        pygame.mixer.music.load("somteste.mp3") #pega a música

    def game_loop(self):
        self.scroll = [0,0]
        yspeed = 0
        GRAVIDADE = 0.5
        opacidade = 0
        self.tutorial = True
        pontuação_maxima = len(self.trash.rects)
        while self.tutorial:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.tutorial = False
                        self.playing = True
                        break
            print('cabra')
            self.tutorial_img = pygame.image.load("tutorial.png")
            self.tutorial_img = pygame.transform.scale(self.tutorial_img,(self.DISPLAY_W, self.DISPLAY_H))
            self.display.blit(self.tutorial_img,(0,0))
            pygame.display.update()
            self.window.blit(self.display, (0,0))
            
        while self.playing:
            if not self.music_playing:
                #tratamento de erro(que humberto pediu, então já coloquei na música)
                try:
                    pygame.mixer.music.play(-1) #música em loop
                    self.music_playing = True #coloca pra tocar a música
                except pygame.error as erro:
                    print(f"Erro ao produzir a música: {erro}")

            self.clock.tick(60)
            # print(self.clock.get_fps()) #Mostrar FPS
            
            self.check_events()
            
            ###Mudança de fase
            
            #Derrota:
            posição_y = self.jogador.rect.y
            if posição_y > 1000:
                print('morreu')
                derrota = True
                while derrota:
                    tela_morte = pygame.image.load(r'assets\tela_morte.png').convert()
                    tela_morte = pygame.transform.scale(tela_morte,(self.DISPLAY_W, self.DISPLAY_H))
                    self.display.blit(tela_morte,(0,0))
                    pygame.display.update()
                    self.window.blit(self.display, (0,0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.restart_level('map_test',0)
                                derrota = False
                
            if self.jogador.arvore and self.Q_Key and self.treecounter >= 5:
                self.Arvores.add_tree(self.jogador.rect.x, self.jogador.rect.y, self.map.rectlist)
                self.treecounter -= 5
            
            self.display.fill((45, 142, 193))
            
            #Show the tree icon
            # if self.treecounter >= 5:
                
            # Camera
            self.scroll[0] += (self.jogador.rect.x+64 - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.jogador.rect.y - self.display.get_height() / 2 - self.scroll[1]) / 15
            
            #Para fixar a câmera em um dos cantos
            # if self.jogador.rect.x < 10*32 and self.scroll[0] > 0:
            #     self.scroll[0] -= 0.5
            # if self.jogador.rect.x < 10*32 and self.scroll[0] < 0:
            #     self.scroll[0] = 0
            
            # if self.jogador.rect.x > 562 and self.scroll[0] > 0:
            #     self.scroll[0] += 0.5
            # if self.jogador.rect.x > 562 and self.scroll[0] > 7*32:
            #     self.scroll[0] = 7*32
                
            #Blit the repeating background
            i = 2
            for background in self.background.images:
                self.display.blit(background,((-300)-self.scroll[0]*i/10,0))
                i += 1
            filtro = pygame.surface.Surface((self.DISPLAY_W,self.DISPLAY_H))
            filtro.set_alpha(opacidade)
            filtro.fill((0,255,255))
            self.display.blit(filtro,(0,0))
            
            #Renderizar o tilemap
            self.display.blit(self.map.surface,(0-self.scroll[0],-self.scroll[1]))
            
            #Atualizar o movimento do jogador
            self.jogador.update(self.SPACE_KEY,self.map.rectlist)
            
            #Renderizar e coletar o lixo
            self.trash.draw(self.display,self.scroll)
            self.Arvores.draw_trees(self.display,self.scroll)
            ######### mentions Trash check later ccelesti
            
            if self.jogador.Flip:
                phisicsrect = pygame.Rect(self.jogador.rect[0]+45,self.jogador.rect[1],60,70) ####### what is the difference bt line 89 and 91?
            else:
                phisicsrect = pygame.Rect(self.jogador.rect[0]+45,self.jogador.rect[1],60,70)
            if phisicsrect.collidelist(self.trash.rects) != -1:
                colidedrect = self.trash.rects[phisicsrect.collidelist(self.trash.rects)]
                # pygame.draw.rect(self.display,(0,0,255),(colidedrect[0]-self.scroll[0],colidedrect[1]-self.scroll[1],32,32)) #####when colision true, it changes colour from red to blue
                if self.E_Key:
                    colideindex = phisicsrect.collidelist(self.trash.rects)
                    self.trash.rects.pop(colideindex)
                    self.trash.trash_sprite.pop(colideindex)
                    self.pontuação += 1
                    self.treecounter += 1
                    opacidade = min(60,opacidade + 3)
            print(self.treecounter)
            # self.draw_text(f"Pontuação: {self.pontuação}", 20, 100, 30)        
            #Renderizar o jogador
            self.jogador.draw(self.display,self.scroll)
            
            #####Barra de pontuação
            #Mudança de cor
            incremento = 255/pontuação_maxima
            if self.pontuação > pontuação_maxima/2:
                cor_pontuação = [min(255,255-(incremento*self.pontuação)*1.2+150),min(255,incremento*self.pontuação*2),0]
            else:
                cor_pontuação = [255,incremento*self.pontuação,0]
            
            #Desenhar a barra
            pygame.draw.rect(self.display,(cor_pontuação),(20,50,self.pontuação*10,20))
            pygame.draw.rect(self.display,(30,30,30),(20,50,pontuação_maxima*10,20),width=2)
            
            #atualizar a tela
            pygame.display.update()
            self.window.blit(self.display, (0,0))
            # print(self.jogador.L_Key,self.jogador.R_key)
            self.reset_keys()


    def restart_level(self,map,state=0):
        self.map = TileMap(f'assets\maps\{map}.csv')
        self.trash = Trash(self.map.toprectlist)
        self.jogador = Player()
        self.pontuação = 0
        self.Arvores = Arvores()
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN:
                        self.START_KEY = True
                    case pygame.K_BACKSPACE:
                        self.BACK_KEY = True
                    case pygame.K_DOWN:
                        self.DOWN_KEY = True
                    case pygame.K_UP:
                        self.UP_KEY = True
                    case pygame.K_SPACE:
                        self.SPACE_KEY = True
                    case pygame.K_e:
                        self.E_Key = True
                    case pygame.K_q:
                        self.Q_Key = True
                        
                    case pygame.K_RIGHT:
                        self.jogador.R_Key = True
                    case pygame.K_LEFT:
                        self.jogador.L_Key = True
                    case pygame.K_LSHIFT:
                        self.jogador.SHIFT = True
                            
                        
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT:
                        self.jogador.L_Key = False
                    case pygame.K_RIGHT:
                        self.jogador.R_Key = False
                    case pygame.K_LSHIFT:
                        self.jogador.SHIFT = False
                        self.jogador.speed_mult = 1
                    case pygame.K_f:
                        match self.fullscreen:
                            case True:
                                pygame.display.toggle_fullscreen()
                                self.fullscreen = False
                                break
                            case False:
                                pygame.display.toggle_fullscreen()
                                self.fullscreen = True
                                break
                    

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY, self.E_Key, self.Q_Key = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color=None, border=False, border_color=(0, 0, 0)):
        if color is None:
            color = self.WHITE
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        font = pygame.font.Font(font_path, size)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        if border:
            # Desenha o texto ao redor da posição original para formar a borda
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if dx != 0 or dy != 0:
                        border_surf = font.render(text, True, border_color)
                        border_rect = border_surf.get_rect()
                        border_rect.center = (x + dx, y + dy)
                        self.display.blit(border_surf, border_rect)

        # Desenha o texto principal por cima
        self.display.blit(text_surface, text_rect)

if __name__ == '__main__':
    from menu import tela_inicial
    tela_inicial()
    jogo = Game()
    jogo.playing = True
    jogo.game_loop()