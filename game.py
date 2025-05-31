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
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.curr_menu = None
        self.jogador = Player()
        self.maplist = ['map_test','map1','map2']
        self.map = TileMap(fr'assets\maps\{self.maplist[0]}.csv')
        self.pontuação = 0
        self.fullscreen = False
        self.Arvores = Arvores()
        self.music_playing = False
        self.mapa = 0
        self.background = Background(5)
        self.treecounter = 0
        self.treeicon = pygame.image.load(r'assets\tree icon.png').convert_alpha()
        self.treeicon = pygame.transform.scale(self.treeicon,(50,50))
        self.times = []
        self.points_to_plant_tree = 5
        
        self.clockicon = pygame.image.load('assets\clock.png').convert_alpha()
        self.clockicon = pygame.transform.scale_by(self.clockicon,.8)
        
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 25)
        pygame.mixer.init() # Inicia a música
        pygame.mixer.music.load("musica.mp3") # Carrega a música

    def game_loop(self):
        global loop_start,opacidade, pontuação_maxima
        loop_start = True
        #Basic variables
        self.scroll = [0,0]
        opacidade = 0
        self.tutorial = True
        self.trash = Trash(self.map.toprectlist)
        pontuação_maxima = len(self.trash.trash_sprite)
        self.time_of_map = 0
        
        #TUtorial
        while self.tutorial:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.time_of_map = 0 #Reinicia o timer
                        self.tutorial = False
                        self.playing = True
                        break
                if event.type == pygame.QUIT:
                    sys.exit()
            self.tutorial_img = pygame.image.load("tutorial.png")
            self.tutorial_img = pygame.transform.scale(self.tutorial_img,(self.DISPLAY_W, self.DISPLAY_H))
            self.display.blit(self.tutorial_img,(0,0))
            pygame.display.update()
            self.window.blit(self.display, (0,0))
            self.time_of_map = 0
        self.timer = pygame.time.Clock()
        
        
        #Main loop of the game
        while self.playing:
            #Play the music of the game
            if not self.music_playing:
                try:
                    pygame.mixer.music.play(-1) # Música em loop
                    self.music_playing = True # Coloca pra tocar a música
                except pygame.error as erro:
                    print(f"Erro ao produzir a música: {erro}")

            # print(self.clock.get_fps()) #Mostrar FPS
            
            self.check_events()
            
            # Loop de derrota:
            self.derrota()
                                
            ### Mudança de fase
            self.mudarfase()
            
            # Verify and plant tree
            if self.jogador.arvore and self.Q_Key and self.treecounter >= self.points_to_plant_tree:
                self.Arvores.add_tree(self.jogador.rect.x, self.jogador.rect.y, self.map.rectlist)
                self.treecounter -= self.points_to_plant_tree
            
            # Preenche a tela com Fill the display with a random color
            self.display.fill((45, 142, 193))
                
            # Camera
            self.scroll[0] += (self.jogador.rect.x+64 - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.jogador.rect.y - self.display.get_height() / 2 - self.scroll[1]) / 15
                            
            #Blit the repeating background
            i = 2 #posição inicial do background
            for background in self.background.images:
                self.display.blit(background,((-500)-self.scroll[0]*i/10,0))
                i += 1
            
            #Filtro de cor
            filtro = pygame.surface.Surface((self.DISPLAY_W,self.DISPLAY_H))
            filtro.set_alpha(opacidade)
            filtro.fill((0,255,255))
            self.display.blit(filtro,(0,0))
            
            #Renderizar o tilemap
            self.display.blit(self.map.surface,(0-self.scroll[0],-self.scroll[1]))
            
            #Atualizar o movimento do jogador
            self.jogador.update(self.SPACE_KEY,self.map.rectlist)
            
            self.trash_verifyandcolect()            
            
            #Show the tree icon
            if self.treecounter >= self.points_to_plant_tree:
                self.display.blit(self.treeicon,(self.DISPLAY_W-70,20))
            # Tree quantity
            if self.treecounter >= self.points_to_plant_tree * 2:
                tree_counter_text = FONTE_MUITO_MAIS_QUE_PEQUENA.render(f'{self.treecounter//5}', True, VERDE)
                xcircle = LARGURA - tree_counter_text.get_width()-10
                ycircle = 27
                TELA.blit(tree_counter_text, (xcircle, ycircle))
                xnum = LARGURA - tree_counter_text.get_width()-6
                ynum = 32
                pygame.draw.circle(self.display, PRETO, (xnum,ynum), 12, 30)
            #Renderizar o jogador
            self.jogador.draw(self.display,self.scroll)
            
            self.barraPontuação()
            
            #Reset the timer if it is the first iteration of the loop:
            #Contador de tempo do mapa
                
            if self.playing: #Para não contar tempo no tutorial
                self.timer.tick() 
                self.time_of_map += self.timer.get_time()
            
            if loop_start == True:
                textRect = self.font.render(str(self.time_of_map/1000),True,(132,176,103)).get_rect()
                self.time_of_map = 0
                loop_start = False
                
            
            #Limit the game to 60 FPS
            self.clock.tick(60)
            
            #Display the time
            self.display.blit(self.font.render(str(round(self.time_of_map/1000,2)),True,(132,176,103)),(70,19)) #TODO Ajust position
            #Display the clock icon
            self.display.blit(self.clockicon,(20,5))
            print(self.times)
            #Para fazer o fundo do texto
            try:
                if textRect.size[0] < self.font.render(str(self.time_of_map/1000),True,(132,176,103)).get_rect().size[0]:
                    textRect = self.font.render(str(self.time_of_map/1000),True,(132,176,103)).get_rect()
            except UnboundLocalError:
                textRect = self.font.render(str(self.time_of_map/1000),True,(132,176,103)).get_rect()
                
            backsurface = pygame.Surface((textRect.size[0]-10,textRect.size[1]+5))
            backsurface.set_alpha(60)
            self.display.blit(backsurface,(65,15))
            #atualizar a tela
            pygame.display.update()
            self.window.blit(self.display, (0,0))
            self.reset_keys()


    def restart_level(self,map,state=0):
        global pontuação_maxima,loop_start,opacidade
        self.map = TileMap(f'assets\maps\{map}.csv')
        opacidade = 0
        self.trash = Trash(self.map.toprectlist)
        pontuação_maxima = len(self.trash.trash_sprite)
        self.jogador = Player()
        self.pontuação = 0
        self.Arvores = Arvores()
        self.treecounter = False
        loop_start = True
        self.time_of_map = 0
        if state == 1:
            self.mapa = 0
        
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
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.SPACE_KEY = True
        
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY, self.E_Key, self.Q_Key = False, False, False, False, False, False, False

    def trash_verifyandcolect(self):
        global opacidade
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
        
    def barraPontuação(self):
        global pontuação_maxima
        #####Barra de pontuação
        #Mudança de cor
        incremento = 255/pontuação_maxima+0.1
        if self.pontuação > pontuação_maxima/2:
            cor_pontuação = [min(255,255-(incremento*self.pontuação)*1.2+150),min(255,incremento*self.pontuação*2),0]
        else:
            cor_pontuação = [255,incremento*self.pontuação,0]
        
        #Desenhar a barra
        larguraDaBarra = 300
        pygame.draw.rect(self.display,(cor_pontuação),(20,50,self.pontuação*larguraDaBarra/pontuação_maxima,20))
        pygame.draw.rect(self.display,(30,30,30),(20,50,larguraDaBarra,20),width=2)
        
    def derrota(self):
        posição_y = self.jogador.rect.y
        if posição_y > 1500:
            derrota = True
            while derrota:
                tela_morte = pygame.image.load(r'assets\tela_morte.png').convert()
                tela_morte = pygame.transform.scale(tela_morte,(self.DISPLAY_W, self.DISPLAY_H))
                self.display.blit(tela_morte,(0,0))
                pygame.display.update()
                self.window.blit(self.display, (0,0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                        self.playing = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.time_of_map = 0 #Reinicia o timer
                            self.restart_level(self.maplist[0],1)
                            derrota = False
    
    
    def mudarfase(self):
        if len(self.trash.rects) == 0 and self.treecounter < self.points_to_plant_tree:
                self.times.append([self.mapa,self.time_of_map])
                self.time_of_map = 0
                self.mapa += 1
                
        while len(self.trash.rects) == 0 and self.treecounter < self.points_to_plant_tree:
            tela_vitória = pygame.image.load(r'assets\tela_vitória.png').convert()
            tela_vitória = pygame.transform.scale(tela_vitória,(self.DISPLAY_W, self.DISPLAY_H))
            tela_fim = pygame.image.load(r'assets\tela_fim.png').convert()
            tela_fim = pygame.transform.scale(tela_fim,(self.DISPLAY_W, self.DISPLAY_H))
            if self.mapa != 3:
                self.display.blit(tela_vitória,(0,0))
            else:
                self.display.blit(tela_fim,(0,0))
            pygame.display.update()
            
            self.window.blit(self.display, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.mapa == len(self.maplist):
                            self.playing = False
                            self.time_of_map = 0
                            self.treecounter = 30
                        else:
                            self.restart_level(self.maplist[self.mapa],0)
                        derrota = False
            
                        
                        
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