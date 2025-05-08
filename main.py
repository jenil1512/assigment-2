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
        
class WaterTile