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
        print(quantidade)
        return self.sprites
        
class Background:
    def __init__(self,copias):
        self.images = []
        files = (file for file in os.listdir(r'assets\background') if os.path.isfile(os.path.join(r'assets\background', file)))
        for file in files:
            path = R'assets\background' + R"\\"
            imagem = pygame.image.load(path + file).convert_alpha()
            superficie = pygame.Surface((imagem.get_width()*copias,imagem.get_height()))#Cria uma superficie para copiar a imagem várias vezes
            imagem.set_colorkey((0,0,0))
            for i in range(copias):
                superficie.blit(imagem,(i*imagem.get_width(),0))
            superficie.set_colorkey((0,0,0))
            self.images.append(superficie)
        for index in range(len(self.images)):
            self.images[index] = pygame.transform.scale_by(self.images[index],2)
        
        print(self.images)
        
        # modifica a escala para preencher a tela do jogo
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
    #Ler CSV e tranformar em lista de listas
    #para cada item colocar um item na lista
    #Renderizar em uma superficie o mapa
    
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
                    self.surface.blit(self.tiles[int(column)],(y*32,x*32))
                    c += 1
                y += 1
            x += 1
            y = 0
        else:
            print(c)
            
    def gettilerects(self):
        self.rectlist = []
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column != '-1':
                    self.rectlist.append((y*32,x*32,32,32))
                y += 1
            x += 1
            y = 0
                
    def gettoprects(self):
        self.toprectlist = []
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column in ('0','1','2','3','12','13','14','15'):
                    self.toprectlist.append((y*32,x*32,32,32))
                y += 1
            x += 1
            y = 0
            
class musica:
    def rodar_musica1():

        pygame.mixer.init() # iniciar mixer
        pygame.mixer.music.load("somteste.mp3") # diretório da música
        pygame.mixer.music.play(-1) # play na música(em loop)        

if __name__ == '__main__':
    t = TileMap(r'assets\maps\map1.csv')
    t.gettilerects()

if __name__ == '__main__':
    B = Background()
    print(B.images)
    
    
