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
PRETO = (0, 0, 0)
VERDE = (100, 200, 20)
VERDE_ESCURO = (0, 150, 0)
VERDE_CREDITOS = (84, 201, 55)
LARANJA = (255, 153, 51)
LARANJA_ESCURO = (205, 102, 0)
VERMELHO = (200, 0, 0)
VERMELHO_ESCURO = (150, 0, 0)
BROWN = (139, 69, 19)
BROWN_ESCURO = (101, 67, 33) 


# Fontes
fonte_grande = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
fonte_pequena = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
fonte_mais_que_pequena = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
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
        texto_surf = fonte_pequena.render(self.texto, True, PRETO)
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
                    return  # retorna ao menu principal
                    rodando = False

        mouse_pos = pygame.mouse.get_pos()
        botao_voltar.verificar_hover(mouse_pos)

        TELA.blit(fundo_creditos, (0, 0))
        TELA.blit(rect_fundo, (LARGURA - 830, 120))

        titulo = fonte_grande.render("AGRADECIMENTOS", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 100 - 30))
        TELA.blit(titulo, titulo_rect)

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
                texto = fonte_mais_que_pequena.render(linha, True, BRANCO)
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
        titulo = fonte_grande.render("REFLORESTA", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//3))
        TELA.blit(titulo, titulo_rect)
        #game.draw_text("REFLORESTA", 40, LARGURA // 2, ALTURA // 3, BRANCO, TELA, border=True, border_color=PRETO)

        # Botões
        botao_iniciar.desenhar(TELA)
        botao_sair.desenhar(TELA)
        botao_creditos.desenhar(TELA)

        pygame.display.flip()
        pygame.time.Clock().tick(60)