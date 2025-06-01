import pygame, random, os
from utils import Spritesheet, TileMap

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.L_Key,self.R_Key,self.Flip = False,False,False
        self.SHIFT = False
        self.load_frames()
        self.rect = pygame.Rect(0,800,32,70)
        self.rect.y = -10
        self.rect.x = -40
        self.current_frame = 0
        self.last_updated = 0 
        self.velocity = 0 
        self.speed = 5
        self.speed_mult = 1
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
        self.velocity_y,self.velocity_x = 0,0
        self.canJump = False
        self.arvore = False
        
        self.joystick = {
            'a':False,
            'x':False,
            'y':False,
            'b':False,
            'up':False,
            'down':False,
            'left':False,
            'right':False,
            'axis':0,
            'run':False
        }

        
    def update(self,jump,tilerects): # Altera a posição, estado e animação do personagem
        self.velocity_x = 0
        self.canJump = False
        self.arvore = False
        if self.L_Key or self.joystick['left'] or self.joystick['axis'] == -1:
            if self.SHIFT or self.joystick['run']:
                self.velocity_x = -self.speed * self.speed_mult
                self.speed_mult = min(1.5, self.speed_mult + 0.1)
            else:
                self.velocity_x = -self.speed
            self.Flip = True
        if self.R_Key or self.joystick['right'] or self.joystick['axis'] == 1:
            if self.SHIFT or self.joystick['run']:
                self.velocity_x = self.speed * self.speed_mult
                self.speed_mult = min(1.5, self.speed_mult + 0.1)
            else:
                self.velocity_x = self.speed
            self.Flip = False
            # self.rect.top -= 15
            
        
        memoryrect = pygame.Rect(self.rect[0],self.rect[1],32,70)
        self.rect.x += self.velocity_x
        phisicsrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
            
        if phisicsrect.collidelistall(tilerects):
            if self.velocity_x > 0:
                    self.rect.x = memoryrect.x
                    
            if self.velocity_x < 0:
                    self.rect.x = memoryrect.x
                
        self.velocity_y += 0.6
        
        memoryrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
        self.rect.y += self.velocity_y
        phisicsrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
            
        if phisicsrect.collidelistall(tilerects):
            if self.velocity_y > 0:
                    self.canJump = True
                    self.velocity_y = 0
                    self.arvore = True
                    self.rect.bottom = memoryrect.bottom
                    
            if self.velocity_y < 0:
                    self.rect.top = memoryrect.top
                    self.velocity_y = 0
        
        if jump or self.joystick['a']:
            if self.canJump:
                self.velocity_y = -15 -abs(self.velocity_x/5)
        
        self.set_state()
        self.animate()
    
    def draw(self,screen,offset):
        screen.blit(self.current_image,(self.rect.x-offset[0],self.rect.y-offset[1]))
        
    def set_state(self):
        self.state = 'idle'
        if self.velocity_x > 0:
            self.Flip = False
            if self.velocity_x > 5:
                self.state = 'run'
            else:
                self.state = 'walk'
        if self.velocity_x < 0:
            self.Flip = True
            if self.velocity_x < -5:
                self.state = 'run'
            else:
                self.state = 'walk'
                
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'idle':  # O personagem fica parado
            if now - self.last_updated > 1000/len(self.idle_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.idle_frames_right)
            if self.current_frame >= len(self.idle_frames_left):
                self.current_frame = 0
            if self.Flip:
                self.current_image = self.idle_frames_left[self.current_frame]
            else:
                self.current_image = self.idle_frames_right[self.current_frame]
        if self.state == 'run':  # O personagem corre
            if now - self.last_updated > 1000/len(self.run_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.run_frames_right)
            if self.Flip:
                self.current_image = self.run_frames_left[self.current_frame]
            else:
                self.current_image = self.run_frames_right[self.current_frame]
                
        if self.state == 'walk':  # O personagem anda
            if now - self.last_updated > 1000/len(self.walk_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.walk_frames_right)
            if self.Flip:
                self.current_image = self.walk_frames_left[self.current_frame]
            else:
                self.current_image = self.walk_frames_right[self.current_frame]
            
    def load_frames(self):
        spritesheet_run = Spritesheet('assets\player\Run.png')
        self.run_frames_right = spritesheet_run.get_sprites()
        self.run_frames_left = []
        for frame in self.run_frames_right:
            self.run_frames_left.append(pygame.transform.flip(frame,True,False))
        
        spritesheet_idle = Spritesheet('assets\player\Idle.png')
        self.idle_frames_right = spritesheet_idle.get_sprites()
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame,True,False))
            
        spritesheet_walk = Spritesheet('assets\player\Walk.png')
        self.walk_frames_right = spritesheet_walk.get_sprites()
        self.walk_frames_left = []
        for frame in self.walk_frames_right:
            self.walk_frames_left.append(pygame.transform.flip(frame,True,False))
        
class Trash(pygame.sprite.Sprite):
    def __init__(self,tilemap):
        self.tiles = tilemap
        self.trash = list()
        self.posições = set()
        self.quantidade = 30
        self.rects = []
        self.trash_sprite = []
        self.images = []

        for file in os.listdir(r'assets\trash'):
            image = pygame.image.load(fr'assets\trash\{file}').convert_alpha()
            image = pygame.transform.scale_by(image, 2)
            self.images.append(image)

        for i in range(self.quantidade):
            posição = random.randint(0,len(tilemap))
            self.posições.add(posição)
        for i in self.posições:
            self.rects.append(pygame.Rect(self.tiles[i-1][0],self.tiles[i-1][1]-32,32,32))
            self.trash_sprite.append(random.randint(0,len(self.images)-1))
    
    def draw(self,display:pygame.Surface, offset):
        for i, trash in enumerate(self.rects):
            image = self.images[self.trash_sprite[i]]
            display.blit(image, (trash.x - offset[0], trash.y - offset[1]))

class Arvores():
    def __init__(self):
        self.tree_list = list()
        self.tree_dict = {}
        self.images = []
        self.frame_counter = 0
        self.counter = 0
        self.manytrees = []
        self.points_to_plant_tree = 5
        self.treecounter = 0
        tree_name = 'ipê roxa'
        for name in ['ipê roxa', 'ipê amarela', 'Growing Tree']:
            if name == 'Growing Tree':
                for file in os.listdir(rf'assets\Arvore\{name}'):
                    image = pygame.image.load(fr'assets\Arvore\{name}\{file}').convert_alpha()
                    image = pygame.transform.scale_by(image,1)
                    self.images.append(image)
                self.manytrees.append(self.images)
                self.images = []
            else:
                for file in os.listdir(rf'assets\Arvore\{name}'):
                    image = pygame.image.load(fr'assets\Arvore\{name}\{file}').convert_alpha()
                    image = pygame.transform.scale_by(image,1.3)
                    self.images.append(image)
                self.manytrees.append(self.images)
                self.images = []
    def add_tree(self, x, y, tilerects):
        # Ajuste o x para alinhar na grade de 32 (mais o offset que já usa)
        tile_x = x - x % 32 + 18
        tile_y = y

        # Criar retângulo da árvore (largura e altura aproximadas da árvore)
        tree_rect = pygame.Rect(tile_x, tile_y, 32, 70)  # Pode ajustar o tamanho, caso necessário

        # Verifica se já tem árvore ali
        if str((tile_x, tile_y)) in self.tree_dict:
            print('já tenho árvore aqui')
            return
        # Se passou nas verificações, adiciona a árvore
        self.tree_list.append([tile_x, tile_y, 0,0,random.randint(0,2)])
        self.tree_dict[str((tile_x, tile_y))] = 1
        self.treecounter -= self.points_to_plant_tree

    # def draw_trees(self, screen: pygame.Surface, offset):
    #     self.frame_counter += 1
    #     grow_frame = self.frame_counter % 3 == 0
    #     self.tree_list.append([x-x%32+18,y,0])
    #     self.tree_dict[str((x-x%32+18,y))] = 1  
          
    def draw_trees (self,screen:pygame.Surface,offset):
        for tree in self.tree_list:
            if tree[4] == 2:
                screen.blit(self.manytrees[tree[4]][tree[2]], (tree[0] - offset[0] -8 , tree[1] - offset[1] - 129))
            else:
                screen.blit(self.manytrees[tree[4]][tree[2]], (tree[0] - offset[0] -8 , tree[1] - offset[1]-95))
            if tree[3] % 30 == 0: # Para atrasar o crescimento da árvore
                tree[2] = min(len(self.manytrees[tree[4]]) - 1, tree[2] + 1)
            tree[3] += 1

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((300,300))
    M = TileMap('assets\maps\map2.csv')
    T = Trash(M.rectlist)