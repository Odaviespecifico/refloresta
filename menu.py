import pygame
import sys

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
VERMELHO = (200, 0, 0)
VERMELHO_ESCURO = (150, 0, 0)
BROWN = (139, 69, 19)
BROWN_ESCURO = (101, 67, 33) 

# Fontes
fonte_grande = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
fonte_pequena = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)

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

def tela_inicial():
    botao_iniciar = Botao(LARGURA//2 - 100, ALTURA//2, 200, 50, "Iniciar", VERDE, VERDE_ESCURO)
    botao_sair = Botao(LARGURA//2 - 100, ALTURA//2 + 70, 200, 50, "Sair", VERMELHO, VERMELHO_ESCURO)
    
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
        
        mouse_pos = pygame.mouse.get_pos()
        botao_iniciar.verificar_hover(mouse_pos)
        botao_sair.verificar_hover(mouse_pos)

        # Fundo com imagem
        TELA.blit(imagem_fundo, (0, 0))
        
        # Título
        titulo = fonte_grande.render("REFLORESTA", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//3))
        TELA.blit(titulo, titulo_rect)

        # Botões
        botao_iniciar.desenhar(TELA)
        botao_sair.desenhar(TELA)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)