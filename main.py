from abc import ABC, abstractmethod

class Tile(ABC):
    '''An abstract class representing a title on the game map. '''
    def __init__(self, x, y):
        ''' Initializes a tile at position(x,y).'''
        self.__x = x
        self.__y = y
        self.__game_object = None
        
    def get_x(self):
        ''' Return the x coordinate of the tile. '''
        return self.__x
    
    def get_y(self):
        ''' Return the y coordinate of the tile. '''
        return self.__y
    
    def set_game_object(self,obj):
        ''' Sets a game object on the tile. '''
        self.__game_object = obj
        
    def get_game_object(self):
        ''' Return the game object on the tile. '''
        return self.__game_object
    
    @abstractmethod
    def display(self):
        pass
    
    def __repr__(self):
        return f"Tile(x={self.__x}, y = {self.__y}, object = {repr(self.__game_object)})"
        
class WaterTile(Tile):
    ''' Represents a water title. '''
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def display(self):
        ''' Returns a character based on the object on the water tile. '''
        obj = self.get_game_object()
        if obj:
            if type(obj).__name__ == "PirateShip":
                return "U" #player's ship
            elif type(obj).__name == "EnemyShip":
                return "u" # Enemy ship
        return " "
    
class LandTile(Tile):
    ''' Represents a land tile that can hold treasure and pirates. '''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__treasure_container = None
        
    def set_treasure_container(self, treasure):
        ''' Sets treasure on the tile. '''
        self.__treasure_container = treasure
        
    def get_treasure_container(self):
        ''' Get the treasure container. '''
        return self.__treasure_container
    
    def display(self):
        ''' Returns a character based o the object on the land tile. '''
        obj = self.get_game_object()
        if obj:
            if type(obj).__name__ == "Pirate":
                if self.__treasure_container:
                    return "X" #pirate and treasure
            return "o" # pirate only
        return "+" # land tile

class Map:
    def __init__(self):
        self.__tiles = []
        try:
            file = open("map.txt","r")
            lines = file.readlines()
            file.close()
        except:
            print("Error")
            return
        
        for y in range(len(lines)):
            row = []
            line = lines[y].strip()
            for x in range (len(line)):
                ch = line[x]
                if ch == "~":
                    tile = WaterTile(x,y)
                elif ch == "+":
                    tile = LandTile(x,y)
                else:
                    tile = None
                row.append(tile)
            self.__tiles.append(row)
            
    def get_tile(self,x,y):
        ''' Returns the tile at the given x and y coordinates. '''
        if y >= 0 and y < len(self.__tiles):
            if x >= 0 and x < len(self.__tiles[y]):
                return self.__tiles[y][x]
        return None
    
    def display_tiles(self):
        ''' Displays the map by printing each tile's symbol. '''
        for row in self.__tiles:
            line = " "
            for tile in row:
                line += tile.display() + " "
            print(line.strip())
            
    def update_game_entities(self):
        pass
    
