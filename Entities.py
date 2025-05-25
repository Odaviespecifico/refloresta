import pygame, random, os
from utils import Spritesheet, TileMap

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.L_Key,self.R_Key,self.Flip = False,False,False
        self.SHIFT = False
        self.load_frames()
        self.rect = pygame.Rect(0,0,32,70)
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
        
    def update(self,jump,tilerects): # Altera a posição, estado e animação do personagem
        self.velocity_x = 0
        self.canJump = False
        self.arvore = False
        if self.L_Key:
            if self.SHIFT:
                self.velocity_x = -self.speed * self.speed_mult
                self.speed_mult = min(2, self.speed_mult + 0.2)
            else:
                self.velocity_x = -self.speed
            self.Flip = True
        if self.R_Key:
            if self.SHIFT:
                self.velocity_x = self.speed * self.speed_mult
                self.speed_mult = min(2, self.speed_mult + 0.2)
            else:
                self.velocity_x = self.speed
            self.Flip = False
            # self.rect.top -= 15
            
        self.rect.x += self.velocity_x
        
        if self.Flip:
            phisicsrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
        else:
            phisicsrect = pygame.Rect(self.rect[0]+40,self.rect[1],32,70)
            
        if phisicsrect.collidelistall(tilerects):
            if self.velocity_x > 0:
                    self.rect.right = tilerects[phisicsrect.collidelist(tilerects)][0] - 40
            if self.velocity_x < 0:
                self.rect.left = pygame.Rect(tilerects[phisicsrect.collidelist(tilerects)]).right -50
                
        self.velocity_y += 0.6
        self.rect.y += self.velocity_y
        
        if self.Flip:
            phisicsrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
        else:
            phisicsrect = pygame.Rect(self.rect[0]+40,self.rect[1],32,70)
            
        if phisicsrect.collidelistall(tilerects):
            if self.velocity_y > 0:
                    self.rect.bottom = pygame.Rect(tilerects[phisicsrect.collidelist(tilerects)]).top
                    self.velocity_y = 0
                    self.canJump = True
                    self.arvore = True
                    
            if self.velocity_y < 0:
                    self.rect.top = tilerects[phisicsrect.collidelist(tilerects)][1]+32
                    self.velocity_y = 0
        
        if jump:
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
        if self.state == 'idle':  # personagem fica parado
            if now - self.last_updated > 1000/len(self.idle_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.idle_frames_right)
            if self.current_frame >= len(self.idle_frames_left):
                self.current_frame = 0
            if self.Flip:
                self.current_image = self.idle_frames_left[self.current_frame]
            else:
                self.current_image = self.idle_frames_right[self.current_frame]
        if self.state == 'run':  # personagem corre
            if now - self.last_updated > 1000/len(self.run_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.run_frames_right)
            if self.Flip:
                self.current_image = self.run_frames_left[self.current_frame]
            else:
                self.current_image = self.run_frames_right[self.current_frame]
                
        if self.state == 'walk':  # personagem anda
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
        self.quantidade = random.randint(20,30)
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
            try:
                self.rects.append(pygame.Rect(self.tiles[i][0],self.tiles[i][1]-32,32,32))
                self.trash_sprite.append(random.randint(0,len(self.images)-1))
            except IndexError:               
                continue
    
    def draw(self,display:pygame.Surface, offset):
        for i, trash in enumerate(self.rects):
            image = self.images[self.trash_sprite[i]]
            display.blit(image, (trash.x - offset[0], trash.y - offset[1]))

class Arvores():
    def __init__(self):
        self.tree_list = list()
        self.tree_dict = {}
        self.images = []
        for file in os.listdir(r'assets\Arvore\Growing Tree'):
            image = pygame.image.load(fr'assets\Arvore\Growing Tree\{file}').convert_alpha()
            image = pygame.transform.scale_by(image,2)
            self.images.append(image)
    def add_tree(self, x,y):
        try: 
            self.tree_dict[str((x-x%32+18,y))]
            print('Já tenho árvore aqui')
        except KeyError:
            self.tree_list.append([x-x%32+18,y,0])
            self.tree_dict[str((x-x%32+18,y))] = 1    
    def draw_trees (self,screen:pygame.Surface,offset):
        for tree in self.tree_list:
            screen.blit(self.images[tree[2]],((tree[0]-offset[0]-152,tree[1]-offset[1]-155)))
            tree[2] = min(len(self.images)-1,tree[2]+1)
        

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((300,300))
    M = TileMap('assets\maps\map2.csv')
    T = Trash(M.rectlist)