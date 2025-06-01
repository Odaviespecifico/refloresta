import pygame
import sys
# import game

pygame.init()

# Dimensões da tela
LARGURA, ALTURA = 1280, 720
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
FONTE_MAIS_QUE_PEQUENA = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 15)
FONTE_MUITO_MAIS_QUE_PEQUENA = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)

# Imagem de fundo
imagem_fundo = pygame.image.load("assets/background/Menu/Background_Refloresta.png")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))  # Ajusta para o tamanho da tela

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_hover): 
        global escolha
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_atual = cor
        escolha = 0
        
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
        
    def selecionado(self,selecionado=False):
        print('seleciinando')
        self.cor_atual = self.cor_hover if selecionado else self.cor
        
        
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

    rect_fundo = pygame.Surface((700,300), pygame.SRCALPHA)
    pygame.draw.rect(rect_fundo, ((0,0,0,180)),(0,0, 700, 300), border_radius=10)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.JOYBUTTONDOWN:
                return
            if evento.type == pygame.KEYDOWN:
                return
        

        TELA.blit(fundo_creditos, (0, 0))
        TELA.blit(rect_fundo, (LARGURA - 990, 120))

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
                "Coord. Patrícia Mergulhão, CCB Social,",
                "Guilherme Enrique, Leonardo Rafael"
                
            ]
        
        for i, linha in enumerate(creditos_texto):
                texto = FONTE_MAIS_QUE_PEQUENA.render(linha, True, BRANCO)
                TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, 120 + i * 30))
                
        pygame.display.flip()
        pygame.time.Clock().tick(60)



def tela_inicial():
    global escolha
    botao_iniciar = Botao(LARGURA//2 - 100, ALTURA//2, 200, 50, "Iniciar", VERDE, VERDE_ESCURO)
    botao_sair = Botao(LARGURA//2 - 100, ALTURA//2 + 140, 200, 50, "Sair", VERMELHO, VERMELHO_ESCURO)
    botao_creditos = Botao(LARGURA//2 - 100, ALTURA//2 + 70, 200, 50, "Créditos", VERDE, VERDE_ESCURO)
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == 0:
                    if escolha == 1:
                        return
                    if escolha == 0:
                        escolha = 1
                    if escolha == 2:
                        creditos()
                    if escolha == 3:
                        pygame.quit()
                        sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if escolha == 1:
                        return
                    if escolha == 0:
                        escolha = 1
                    if escolha == 2:
                        creditos()
                    if escolha == 3:
                        pygame.quit()
                        sys.exit()
            if evento.type == pygame.JOYHATMOTION:
                if evento.value[1] == 1:
                    escolha = (escolha - 1) % 4
                    print(escolha)
                if evento.value[1] == -1:
                    escolha = (escolha + 1) % 4
                    print(escolha)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    escolha = (escolha + 1) % 4
                if evento.key == pygame.K_UP:
                    escolha = (escolha - 1) % 4
        match escolha:
            case 0:
                botao_iniciar.cor_atual = VERDE
                botao_creditos.cor_atual = VERDE
                botao_sair.cor_atual = VERMELHO
            case 1:
                botao_iniciar.cor_atual = VERDE_ESCURO
                botao_creditos.cor_atual = VERDE
                botao_sair.cor_atual = VERMELHO
            case 2:
                botao_iniciar.cor_atual = VERDE
                botao_creditos.cor_atual = VERDE_ESCURO
                botao_sair.cor_atual = VERMELHO
            case 3:
                botao_iniciar.cor_atual = VERDE
                botao_creditos.cor_atual = VERDE
                botao_sair.cor_atual = VERMELHO_ESCURO
        

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