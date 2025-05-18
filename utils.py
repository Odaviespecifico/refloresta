#Spritesheet
import pygame   

class Spritesheet:
    def __init__(self, filename,width=128,height=70):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.sprite_sheet.set_colorkey((0,0,0))
        self.width = width
        self.height = height
        self.sprites = []
        
    def get_sprite(self,x,y,width=128,height=70):
        sprite = pygame.Surface((width,height))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        return sprite
    
    def get_sprites(self):
        quantidade = int(self.sprite_sheet.get_width()/self.width)
        for sprite in range(quantidade):
            self.sprites.append(self.get_sprite(sprite*128,0))
        print(quantidade)
        return self.sprites
        
        
if __name__ == '__main__':
    print('teste')
    run = Spritesheet('assets\player\Run.png')
    run.get_sprites(1)
    
    idle = Spritesheet('assets\player\Idle.png')
    print(idle.sprites)
    idle.get_sprites(1)
