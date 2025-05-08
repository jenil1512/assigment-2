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
    
