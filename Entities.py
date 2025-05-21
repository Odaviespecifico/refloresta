import pygame, random
from utils import Spritesheet
from tiles import TileMap

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.L_Key,self.R_Key,self.Flip = False,False,False
        self.load_frames()
        self.rect = pygame.Rect(32,0,32,70)
        self.rect.y = 360 - 80
        self.current_frame = 0
        self.last_updated = 0 
        self.velocity = 0 
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
        self.velocity_y,self.velocity_x = 0,0
        
    def update(self,jump,tilerects): # Altera a posição, estado e animação do personagem
        self.velocity_x = 0
        if self.L_Key:
            self.velocity_x = -10
            self.Flip = True
        if self.R_Key:
            self.velocity_x = 10
            self.Flip = False
        if jump:
            self.velocity_y = -15
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
                
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y
        
        if self.Flip:
            phisicsrect = pygame.Rect(self.rect[0]+50,self.rect[1],32,70)
        else:
            phisicsrect = pygame.Rect(self.rect[0]+40,self.rect[1],32,70)
            
        if phisicsrect.collidelistall(tilerects):
            if self.velocity_y > 0:
                    self.rect.bottom = pygame.Rect(tilerects[phisicsrect.collidelist(tilerects)]).top
                    self.velocity_y = 0
                    
            if self.velocity_y < 0:
                    self.rect.top = tilerects[phisicsrect.collidelist(tilerects)][1]+32
                    self.velocity_y = 0
        
        
        
        self.set_state()
        self.animate()
        
    def draw(self,screen,offset):
        screen.blit(self.current_image,(self.rect.x-offset[0],self.rect.y-offset[1]))
        
    def set_state(self):
        self.state = 'idle'
        if self.velocity_x > 0:
            self.Flip = False
            self.state = 'run'
        if self.velocity_x < 0:
            self.Flip = True
            self.state = 'run'
            
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
        
    
class Trash(pygame.sprite.Sprite):
    def __init__(self,tilemap):
        self.tiles = tilemap
        self.posições = set()
        self.quantidade = random.randint(20,30)
        self.rects = []
        for i in range(self.quantidade):
            posição = random.randint(0,len(tilemap))
            self.posições.add(posição)    
        for i in self.posições:
            self.rects.append(pygame.Rect(self.tiles[i][0],self.tiles[i][1]-32,32,32))
        
    
    def draw(self,display:pygame.Surface,offset,):
        for i in self.rects:
            pygame.draw.rect(display,(255,0,45),(i[0]-offset[0],i[1]-offset[1],32,32))
            
        

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((300,300))
    M = TileMap('assets\maps\map2.csv')
    T = Trash(M.rectlist)