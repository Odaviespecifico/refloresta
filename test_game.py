import pygame
from utils import Spritesheet

# Inicializar pygame
pygame.init()

# Configurar o display
WIDTH, HEIGHT = 255, 150
canvas = pygame.Surface((WIDTH, HEIGHT))
window = pygame.display.set_mode((WIDTH, HEIGHT),flags=pygame.SCALED)
pygame.display.set_caption("Sprite Animation")

# Carregar sprites
run = Spritesheet(r'C:\Users\Davi\Documents\Progamação\refloresta\assets\player\Run.png')
runSprites = run.get_sprites(1)  # Assuming this returns a list of sprites
sprite_count = len(runSprites)

idle = Spritesheet('assets\player\Idle.png')
idleSprites = idle.get_sprites(1)

# Variáveis de animação
i = 0
clock = pygame.time.Clock()
FPS = 24  # Controla velocidade da animação

animation = 0

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if animation == 0:
                    animation = 1
                else:
                    animation = 0
    
    # Clear canvas
    canvas.fill((255, 255, 255)) 
    
    # Desenhar sprite atual (centralizada)
    sprite_rect = idleSprites[i].get_rect(center=(WIDTH//2, HEIGHT//2))
    canvas.blit(idleSprites[i], sprite_rect)
    
    # Atualizar frame de animação
    i = (i + 1) % len(idleSprites)  # This will loop back to 0 automatically
    
    # Atualizar display
    window.blit(canvas, (0, 0))
    pygame.display.flip()  # You don't need both flip() and update()
    
    # Controlar a taxa de frames
    clock.tick(FPS)

pygame.quit()