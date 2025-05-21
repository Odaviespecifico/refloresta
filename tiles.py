import pygame, csv, os
        
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
                
    
        
if __name__ == '__main__':
    t = TileMap(r'assets\maps\map1.csv')
    t.gettilerects()