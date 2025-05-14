import pygame
import time
  
#Variáveis básicas: 
BACKGROUND_COLOR = (50, 120, 180)
ALTURA = 360
LARGURA = 640
SPEED = 1.5
GRAVIDADE = 0.2
TELA = pygame.display.set_mode((LARGURA, ALTURA),flags=pygame.SCALED)
 
x_speed = 0
y_speed = 0
dx=0

relogio = pygame.time.Clock()

fullscreen = True 
# Set the caption of the screen 
pygame.display.set_caption('Refloresta') 


# Variable to keep our game loop running 
running = True
playersize = [32, 64]
playerpos = [0, 0]

chao = pygame.Rect(10,340,500,5)
bloco = pygame.Rect(40,300,50,50)
bloco2 = pygame.Rect(200,150,50,50)
bloco3 = pygame.Rect(350,150,50,50)
bloco4 = pygame.Rect(500,150,50,50)
objetos = [chao,bloco,bloco2,bloco3,bloco4]
        
#Atualizar o movimento
colisions =[False,False,False,False] #Top bottom left right
def move(dx, dy):   
    global colisions,y_speed
    for ojeto in objetos:
        playerpos[1] += dy
        player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
        if player.collidelist(objetos) != -1:
            if dy > 0:
                colisions[1] = True
                player.bottom = objetos[player.collidelist(objetos)].top + 1
                playerpos[1] = player.top
            if dy < 0:
                print(dy)
                # Colisão superior
                colisions[0] = True
                y_speed = 1
                dy = 1
            
        for ob in objetos:
            if player.bottom == ob.top:
                pass
            else:
                pass
            
        playerpos[0] += dx
        player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
        for colision in list(player.collidelistall(objetos)):
            if player.collidelist(objetos) != -1 and player.bottom != objetos[colision].top + 1:
                if dx > 0 and not colisions[0]:
                    colisions[2] = True
                    player.right = objetos[colision].left
                    playerpos[0] = player.left
                if dx < 0 and not colisions[0]: 
                    colisions[3] = True
                    player.left = objetos[colision].right
                    playerpos[0] = player.left
        if dx == 0:
            colisions[2],colisions[3] = False,False
        if dy == 0:
            colisions[0],colisions[1] = False,False 
        print(colisions)
idle_spritesheet = pygame.image.load(r"assets\player\Idle.png")
run_spritesheet = pygame.image.load(r"assets\player\run.png")
#width 128
#height 64
def load_sprite_sheet(sheet, frame_width=128, frame_height=67):
    sheet_rect = sheet.get_rect()
    frames = []
    for i in range(sheet_rect.width // frame_width):
        frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

#Variáveis básicas da animação
idle_frames = load_sprite_sheet(idle_spritesheet)
run_frames = load_sprite_sheet(run_spritesheet)

frame = 0
frame_index = 0
animation_speed = 8

flip = False

animation = 0

# game loop 
while running: 
    TELA.fill(BACKGROUND_COLOR) #Clear the screen
# for loop through the event queue   
    mudar = True
    
    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False

    #For the user input
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] and mudar == True:
        animation = 1
    elif mudar == True:
        animation = 0
    
    #Handle key presses
    x_speed = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    
    if flip == False and keys[pygame.K_LEFT]:
        for i in range(len(idle_frames)):
            idle_frames[i] = pygame.transform.flip(idle_frames[i],True,False)
        for i in range(len(run_frames)):
            run_frames[i] = pygame.transform.flip(run_frames[i],True,False)
        flip = True
    if flip == True and keys[pygame.K_RIGHT]:
        for i in range(len(idle_frames)):
            idle_frames[i] = pygame.transform.flip(idle_frames[i],True,False)
        for i in range(len(run_frames)):
            run_frames[i] = pygame.transform.flip(run_frames[i],True,False)
        flip = False
    
    player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
    if player.collidelist(objetos) != -1:
        if keys[pygame.K_SPACE]:
            y_speed = -4
        else:
            y_speed = 0
            
    if player.collidelist(objetos) == -1:
        y_speed += GRAVIDADE
    
    move(x_speed,y_speed)
    #Player
    # pygame.draw.rect(TELA,(255,255,0),(playerpos[0], playerpos[1], playersize[0], playersize[1]))
    
    #chão
    for i in objetos:
        pygame.draw.rect(TELA,(255,255,255),i)
    #Animação do personagem
    
    match animation:
        case 0:
            if frame_index % animation_speed == 0:
                if frame < len(idle_frames)-1 and mudar == True:
                    frame += 1
                    mudar = False
                if frame and mudar == True:
                    frame = 0
                    mudar = False
            frame_index += 1
            if frame >= len(idle_frames):
                frame = 0
            TELA.blit(idle_frames[frame],(playerpos[0]-43,playerpos[1]-5))
        case 1:
            if frame_index % animation_speed == 0:
                if frame < len(run_frames)-1 and mudar == True:
                    frame += 1
                    mudar = False
                if frame and mudar == True:
                    frame = 0
                    mudar = False
            frame_index += 1
            TELA.blit(run_frames[frame],(playerpos[0]-43,playerpos[1]-5))

    pygame.display.flip() 
    relogio.tick(60)