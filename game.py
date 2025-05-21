import pygame
from menu import *
from Entities import Player
from utils import Background
from tiles import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        scale = 50
        self.DISPLAY_W, self.DISPLAY_H = 16*scale, 9*scale
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)),flags=pygame.SCALED)
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.background = Background()
        self.jogador = Player()
        self.map = TileMap('assets\maps\map1.csv')
        
    def game_loop(self):
        self.scroll = [0,0]
        while self.playing:
            
            self.clock.tick(60)
            
            self.check_events()
            if self.START_KEY:
                self.playing= False
            
            self.display.fill(self.WHITE)
            
            #Camera
            camera_offset = [
                +self.jogador.rect.centerx - self.display.get_rect().centerx,
                +self.jogador.rect.centery - self.display.get_rect().centery
            ]
            
            self.scroll[0] += (self.jogador.rect.x+64 - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.jogador.rect.y - self.display.get_height() / 2 - self.scroll[1]) / 30
            
            #Blit the repeating background
            for background in self.background.images:
                self.display.blit(background,((0),0))
            
            self.display.blit(self.map.surface,(0-self.scroll[0],-32*6))
            
            self.jogador.update()
            
            self.jogador.draw(self.display,self.scroll)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
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
                    case pygame.K_RIGHT:
                        self.jogador.R_Key = True
                    case pygame.K_LEFT:
                        self.jogador.L_Key = True
                        
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT:
                        self.jogador.L_Key = False
                    case pygame.K_RIGHT:
                        self.jogador.R_Key = False
                    

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)




