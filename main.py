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
        