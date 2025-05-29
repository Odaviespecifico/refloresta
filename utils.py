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
    
    def get_tile_sprites(self):
        for y in range(16):
            for x in range(16):
                self.sprites.append(self.get_sprite(x*32,y*32,32,32))
                print(x,y)
                
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
        self.spritesheet = Spritesheet(r'assets\Tiles\tilesets\TX Tileset Ground.png',32,32)
        self.spritesheet.get_tile_sprites()
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
                    print(self.spritesheet.sprites)
                    self.surface.blit(self.spritesheet.sprites[int(column)],(y*32,x*32))
                    c += 1
                y += 1
            x += 1
            y = 0
        else:
            pass
        
        
    def gettilerects(self):
        self.rectlist = []
        noncolide_rects = {16,17,18,32,33,34,64,65,66,80,81,82,96,98,74,75,76,72,77,79,88,90,91,92,93,95,102,103,104,106,107,108,109,110,111,116,118,119,120,122,123,124,125,126,127,132,134,136,137,138,139,140,141,
                           143,148,150,152,153,154,155,156,157,159,164,165,166,167,168,171,173,175,
                           180,181,182,183,184,187,189,191,
                           196,197,198,199,200,202,205,
                           212,213,214,215,216,218,228,230,231,232,234,
                           237,238,239,
                           244,246,247,248,250,253,254,255,-1}
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if int(column) not in noncolide_rects:
                    self.rectlist.append((y*32,x*32,32,32))
                y += 1
            x += 1
            y = 0
                
    def gettoprects(self):
        self.toprectlist = []
        grass_rects = [0,1,2,4,5,7,9,10,12,13,52,54,55,56,57,58,59,60,61,62,63,84,86,87,89,94,97,117,121,128,130,149,151,158,192,193,194,186,217,219,220,222,223,224,225,226,245,249,251] # Onde o lixo pode spawnar
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if int(column) in grass_rects:
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
    
    
