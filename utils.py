# Spritesheet
import pygame, csv, os

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
        return self.sprites
        
class Background:
    def __init__(self,copias):
        print('carregando o fundo')
        self.images = []
        files = (file for file in os.listdir(r'assets\background') if os.path.isfile(os.path.join(r'assets\background', file)))
        for file in files:
            print('file')
            path = R'assets\background' + R"\\"
            imagem = pygame.image.load(path + file).convert()
            superficie = pygame.Surface((imagem.get_width()*copias,imagem.get_height())) # Cria uma superfície para copiar a imagem várias vezes
            for i in range(copias):
                superficie.blit(imagem,(i*imagem.get_width(),0))
            superficie.set_colorkey((0,0,0))
            self.images.append(superficie)
        for index in range(len(self.images)):
            self.images[index] = pygame.transform.scale_by(self.images[index],0.3)
        
        
        # Modifica a escala para preencher a tela do jogo
        self.rect = self.images[0].get_rect()
        
class TileMap():
    def __init__(self,map):
        self.map = map
        self.tilemap = self.ler_csv()
        self.surface = pygame.Surface((10000,10000))
        self.surface.set_colorkey((0,0,0))
        self.tiles = []
        for tileimage in os.listdir('assets\Tiles'):
            self.tiles.append(pygame.image.load(fr'assets\Tiles\{tileimage}').convert_alpha())
        self.tiles.pop()
        self.putinasurface()
        self.gettilerects()
        self.gettoprects()
    # Ler CSV e tranformar em lista de listas
    # Para cada item colocar um item na lista
    # Renderizar o mapa em uma superfície 
    
    def ler_csv(self):
        tilemap = []
        with open(self.map,'r') as map:
            for row in csv.reader(map,delimiter=','):
                tilemap.append(row)
        return tilemap

    def putinasurface(self):
        x,y,c = 0,0,0
        for line in self.tilemap:
            for column in line:
                if column != '-1':
                    if column == '25':
                        self.surface.blit(self.tiles[-1],(y*32,x*32))
                    else:
                        self.surface.blit(self.tiles[int(column)],(y*32,x*32))
                    c += 1
                y += 1
            x += 1
            y = 0
        else:
            pass
        
        
    def gettilerects(self):
        self.rectlist = []
        noncolide_rects = {'4','14','15','11','-1'}
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column not in noncolide_rects:
                    self.rectlist.append((y*32,x*32,32,32))
                y += 1
            x += 1
            y = 0
                
    def gettoprects(self):
        self.toprectlist = []
        grass_rects = ['1','2','0','13','18','20','21','22','23','24','25'] # Onde o lixo pode spawnar
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column in grass_rects:
                    self.toprectlist.append((y*32,x*32,32,32))
                y += 1
            x += 1
            y = 0
            
class musica:
    def rodar_musica1():

        pygame.mixer.init() # Iniciar mixer
        pygame.mixer.music.load("somteste.mp3") # Diretório da música
        pygame.mixer.music.play(-1) # Play na música (em loop)

if __name__ == '__main__':
    t = TileMap(r'assets\maps\map1.csv')
    t.gettilerects()

if __name__ == '__main__':
    B = Background()
    
    
