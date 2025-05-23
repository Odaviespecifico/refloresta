import pygame
from menu import *
from Entities import Player,Trash,Arvores
from utils import Background,TileMap

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        scale = 60
        self.DISPLAY_W, self.DISPLAY_H = 16*scale, 9*scale
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)),flags=pygame.SCALED)
        # self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)),flags=pygame.FULLSCREEN|pygame.SCALED)
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.tutorial_screen = Tutorial(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.background = Background(5)
        self.jogador = Player()
        self.map = TileMap('assets\maps\map2.csv')
        self.trash = Trash(self.map.toprectlist)
        self.pontuação = 0
        self.fullscreen = False
        self.Arvores = Arvores()
        self.music_playing = False
        pygame.mixer.init() #inicia música
        pygame.mixer.music.load("somteste.mp3") #pega a música

    def game_loop(self):
        self.scroll = [0,0]
        yspeed = 0
        GRAVIDADE = 0.5
        opacidade = 0
        self.tutorial = True
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
            print(self.clock.get_fps()) #Mostrar FPS
            
            self.check_events()
            if self.START_KEY:
                self.playing= False
            
            
            if self.jogador.arvore and self.Q_Key:
                self.Arvores.add_tree(self.jogador.rect.x,self.jogador.rect.y)
            
            self.display.fill((45, 142, 193))
            
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
            
            if self.jogador.Flip:
                phisicsrect = pygame.Rect(self.jogador.rect[0]+45,self.jogador.rect[1],60,70)
            else:
                phisicsrect = pygame.Rect(self.jogador.rect[0]+45,self.jogador.rect[1],60,70)
            if phisicsrect.collidelist(self.trash.rects) != -1:
                colidedrect = self.trash.rects[phisicsrect.collidelist(self.trash.rects)]
                pygame.draw.rect(self.display,(0,0,255),(colidedrect[0]-self.scroll[0],colidedrect[1]-self.scroll[1],32,32))
                if self.E_Key:
                    self.trash.rects.pop(phisicsrect.collidelist(self.trash.rects))
                    self.pontuação += 1
                    opacidade = min(60,opacidade + 3)

            self.draw_text(f"Pontuação: {self.pontuação}", 20, 100, 30)        
            #Renderizar o jogador
            self.jogador.draw(self.display,self.scroll)
            
            #atualizar a tela
            pygame.display.update()
            self.window.blit(self.display, (0,0))
            # print(self.jogador.L_Key,self.jogador.R_key)
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                
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

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)




