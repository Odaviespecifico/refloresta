import pygame, csv, os
        
class TileMap():
    def __init__(self,map):
        self.map = map
        self.tilemap = self.ler_csv()
        self.surface = pygame.Surface(((len(self.tilemap[0])+1)*32,(len(self.tilemap)+1)*32))
        self.surface.set_colorkey((0,0,0))
        self.tiles = []
        for tileimage in os.listdir('assets\Tiles'):
            self.tiles.append(pygame.image.load(fr'assets\Tiles\{tileimage}'))
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
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column != '-1':
                    print(self.tiles[int(column)])
                    print(x,y)
                    self.surface.blit(self.tiles[int(column)],(y*32,x*32-32*6))
                else:
                    print('sou vazio')
                y += 1
            x += 1
            y = 0
            
    def gettilerects(self):
        print(self.tilemap)
        self.rectlist = []
        x,y = 0,0
        for line in self.tilemap:
            for column in line:
                if column != '-1':
                    self.rectlist.append((y*32,x*32-32*6,32,32))
                else:
                    print('sou vazio')
                y += 1
            x += 1
            y = 0
        print(self.rectlist)
                
    
        
if __name__ == '__main__':
    t = TileMap(r'assets\maps\map1.csv')
    t.gettilerects()