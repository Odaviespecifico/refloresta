import pygame
from utils import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.L_Key,self.R_Key,self.Flip = False,False,False
        self.load_frames()
        self.rect = self.idle_frames_right[0].get_rect()
        self.rect.y = 360 - 80
        self.current_frame = 0
        self.last_updated = 0 
        self.velocity = 0 
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
        
    def update(self): # Altera a posição, estado e animação do personagem
        self.velocity = 0
        if self.L_Key:
            self.velocity = -1
            self.Flip = True
        if self.R_Key:
            self.velocity = 1
            self.Flip = False
        self.rect.x += self.velocity
        self.set_state()
        self.animate()
        
    def draw(self,screen):
        screen.blit(self.current_image,self.rect)
        
    def set_state(self):
        self.state = 'idle'
        if self.velocity > 0:
            self.Flip = False
            self.state = 'run'
        if self.velocity < 0:
            self.Flip = True
            self.state = 'run'
        print(self.Flip)
            
    def animate(self):
        
        now = pygame.time.get_ticks()
        if self.state == 'idle':  # personagem fica parado
            if now - self.last_updated > 1000/len(self.idle_frames_right):
                self.last_updated = now
                self.current_frame = (self.current_frame+1) % len(self.idle_frames_right)
            if self.current_frame >= len(self.idle_frames_left):
                self.current_frame = 0
            if self.Flip:
                print(self.current_frame)
                self.current_image = self.idle_frames_left[self.current_frame]
            else:
                print(self.current_frame)
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
        print(self.idle_frames_left)
        
    