import pygame
import sys
#import game

pygame.init()

# Dimensões da tela
LARGURA, ALTURA = 960, 540
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Refloresta")


# Cores
BRANCO = (255, 255, 255)
BROWN = (139, 69, 19)
BROWN_ESCURO = (101, 67, 33) 
LARANJA = (255, 153, 51)
LARANJA_ESCURO = (205, 102, 0)
VERDE = (100, 200, 20)
VERDE_CREDITOS = (84, 201, 55)
VERDE_ESCURO = (0, 150, 0)
VERMELHO = (200, 0, 0)
VERMELHO_ESCURO = (150, 0, 0)
PRETO = (0, 0, 0)

# Fontes
FONTE_GRANDE = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
FONTE_PEQUENA = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
FONTE_MAIS_QUE_PEQUENA = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)

# Imagem de fundo
imagem_fundo = pygame.image.load("assets/background/Menu/Background_Refloresta.png")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))  # Ajusta para o tamanho da tela

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_hover): 
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_atual = cor
        
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor_atual, self.rect)
        pygame.draw.rect(superficie, PRETO, self.rect, 2)
        texto_surf = FONTE_PEQUENA.render(self.texto, True, PRETO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def verificar_clique(self, pos):
        return self.rect.collidepoint(pos)
    
    def verificar_hover(self, pos):
        self.cor_atual = self.cor_hover if self.rect.collidepoint(pos) else self.cor

# def desenhar_guia(self): # Desenha a tela de guia        
#     if self.background:
#         self.tela.blit(self.background, (0, 0)) # Desenha o fundo
#             # Painel de fundo (retangulo preto com opacidade)
#         painel = pygame.Surface((600, 380), pygame.SRCALPHA) #to do  (opacidade do fundo)
#         painel.fill((*VERMELHO["PRETO"], 180))  # Preto com opacidade
#         self.tela.blit(painel, (self.largura_tela // 2 - 300, 215))
#     else:
#         self.tela.fill(VERMELHO["AZUL"])
        
def desenhar_texto_com_borda(texto, fonte, cor_texto, cor_borda, x, y, superficie):
    texto_base = fonte.render(texto, True, cor_texto)
    texto_borda = fonte.render(texto, True, cor_borda)
    texto_rect = texto_base.get_rect(center=(x, y))

    # Desenha a borda em 8 direções ao redor do texto
    for dx in [-3, 0, 3]:
        for dy in [-3, 0, 3]:
            if dx != 0 or dy != 0:
                superficie.blit(texto_borda, texto_rect.move(dx, dy))

    superficie.blit(texto_base, texto_rect)
    
def creditos():
    rodando = True

    fundo_creditos = pygame.image.load("assets/background/Menu/Background_Refloresta.png").convert()
    fundo_creditos = pygame.transform.scale(fundo_creditos, (LARGURA, ALTURA))
    botao_voltar = Botao(LARGURA//2 - 100, ALTURA - 100, 200, 50, "Voltar", VERDE, VERDE_ESCURO)

    rect_fundo = pygame.Surface((700, 300), pygame.SRCALPHA)
    pygame.draw.rect(rect_fundo, (*VERDE_ESCURO, 180), (0,0, 700, 300), border_radius=10)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.verificar_clique(evento.pos):
                    return  # Retorna para o menu principal
                    rodando = False

        mouse_pos = pygame.mouse.get_pos()
        botao_voltar.verificar_hover(mouse_pos)

        TELA.blit(fundo_creditos, (0, 0))
        TELA.blit(rect_fundo, (LARGURA - 830, 120))

        desenhar_texto_com_borda("AGRADECIMENTOS", FONTE_GRANDE, BRANCO, PRETO, LARGURA//2, 100 - 30, TELA)
        #titulo_rect = titulo.get_rect(center=(LARGURA//2, 100 - 30))
        #TELA.blit(titulo, titulo_rect)

        creditos_texto = [
                "",
                "Integrantes:",
                "Camila Moura, Davi Lucas, Enrico Reno",
                "Samuel Victor, José Miguel, Dheferson Dhone",
                "",
                "",
                "Agradecimentos especiais:",
                ""
                "Coord. Patrícia Mergulhão, CCB Social, Guilherme Enrique, ",
                "Leonardo Rafael"
                
            ]
        
        for i, linha in enumerate(creditos_texto):
                texto = FONTE_MAIS_QUE_PEQUENA.render(linha, True, BRANCO)
                TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, 120 + i * 30))
                
        botao_voltar.desenhar(TELA)
        pygame.display.flip()
        pygame.time.Clock().tick(60)



def tela_inicial():
    botao_iniciar = Botao(LARGURA//2 - 100, ALTURA//2, 200, 50, "Iniciar", VERDE, VERDE_ESCURO)
    botao_sair = Botao(LARGURA//2 - 100, ALTURA//2 + 140, 200, 50, "Sair", VERMELHO, VERMELHO_ESCURO)
    botao_creditos = Botao(LARGURA//2 - 100, ALTURA//2 + 70, 200, 50, "Créditos", VERDE, VERDE_ESCURO)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.verificar_clique(evento.pos):
                    return
                if botao_sair.verificar_clique(evento.pos):
                    pygame.quit()
                    sys.exit()
                if botao_creditos.verificar_clique(evento.pos):
                    creditos()
                      
    
        mouse_pos = pygame.mouse.get_pos()
        botao_iniciar.verificar_hover(mouse_pos)
        botao_sair.verificar_hover(mouse_pos)
        botao_creditos.verificar_hover(mouse_pos)

        # Fundo com imagem
        TELA.blit(imagem_fundo, (0, 0))
        
        # Título
        #titulo = FONTE_GRANDE.render("REFLORESTA", True, BRANCO)
        #titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//3))
        #TELA.blit(titulo, titulo_rect)
        desenhar_texto_com_borda("REFLORESTA", FONTE_GRANDE, BRANCO, PRETO, LARGURA//2, ALTURA//3, TELA)

        # Botões
        botao_iniciar.desenhar(TELA)
        botao_sair.desenhar(TELA)
        botao_creditos.desenhar(TELA)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
game_playing = False
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class Tutorial(Menu):
    global game_playing
    def __init__(self, game):
        Menu.__init__(self, game)
        self.menu = Menu
        self.tutorial_img = pygame.image.load("tutorial.png")
        self.tutorial_img = pygame.transform.scale(self.tutorial_img,(self.game.DISPLAY_W, self.game.DISPLAY_H))
    
    def display_menu(self):
        global game_playing
        self.tutorial_run = True
        # while self.tutorial_run:
        #     self.game.check.events()
        #     if self.game.START_KEY or self.game.BACK_KEY:
        #         self.tutorial_run = False
        #         self.game.playing = True
        #         break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    game_playing = True
                    
        self.game.display.blit(self.tutorial_img, (0, 0))
        self.blit_screen()
        
            
class MainMenu(Menu):
    global game_playing
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.tutorialx, self.tutorialy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.tutorial_screen = Tutorial(game)

    def display_menu(self):
        global game_playing
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input() # Verifica qual opção o jogador selecionou
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('ReFloresta', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Começar jogo", 20, self.startx, self.starty)
            self.game.draw_text("Opções", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Créditos", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Tutorial", 20, self.tutorialx, self.tutorialy)
            self.draw_cursor()
            self.blit_screen()
            
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Opções', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controles", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Créditos', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Feito por Davi', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()