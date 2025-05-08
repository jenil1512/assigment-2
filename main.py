from abc import ABC, abstractmethod

class Tile(ABC):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__game_object = None
        
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_game_object(self,obj):
        self.__game_object = obj
        
    def get_game_object(self):
        return self.__game_object
    
    @abstractmethod
    def display(self):
        pass
    
    def __repr__(self):
        return f"Tile(x={self.__x}, y = {self.__y}, object = {repr(self.__game_object)})"
        
class WaterTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def display(self):
        obj = self.get_game_object()
        if obj:
            if type(obj).__name__ == "PirateShip":
                return "U" #player's ship
            elif type(obj).__name == "EnemyShip":
                return "u" # Enemy ship
        return " "
    
class LandTile(Tile):
    