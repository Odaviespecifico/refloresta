# Spritesheet
import pygame,os

class Spritesheet:
    def __init__(self, filename,width=128,height=70):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
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
        
class Background:
    def __init__(self):
        self.images = []
        for image in os.listdir(R'assets\background'):
            path = R'assets\background' + R"\\"
            self.images.append(pygame.image.load(path + image))
        print(self.images)
        
        # modifica a escala para preencher a tela do jogo
        self.rect = self.images[0].get_rect()
            
if __name__ == '__main__':
    B = Background()
    print(B.images)
    
    
