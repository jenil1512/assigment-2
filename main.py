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
    
    def main():
        map = Map()
        choice = None
        
        while choice != "quit":
            if choice == 'w':
                map.get_player().move(0, -1)
            elif choice == 'a':
                map.get_player().move(-1, 0)
            elif choice == 's':
                map.get_player().move(0, 1)
            elif choice == 'd':
                map.get_player().move(1, 0)
            elif choice == 'dig':
                map.get_player().dig()
                
            map.display_tiles()
            choice = input("Enter w, a, s, d, dig, or quit: ")
            map.update_game_entities()
        
        print("Goodbye")
        
    if __name__ == "__main__":
        main()
    
class GameEntity:
    '''A parent class pirate and ship.'''
    def __init__(self, x=0, y=0, health=100):
        self.__x = x
        self.__y = y
        self.set_health(health)
        self.__treasure = []
        
    def move(self, dx, dy):
        ''' Move the entity by dx and dy. '''
        self.__x += dx
        self.__y += dy
        
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_health(self):
        ''' Returns the health value. '''
        return self.__health
    
    def set_health(self, health):
        ''' Sets the health if it is a positive integer.'''
        if type(health) == int and health >= 0:
            self.__health = health
        else:
            print("error: health must be a positive integer.")
            
    def is_alive(self):
        ''' Checks if the entity is alive. '''
        return self.__health > 0
    
    def add_treasure(self, treasure):
        ''' Add a treasure. '''
        if type(treasure).__name__ == "Treasure":
            self.__treasure.append(treasure)
        else:
            print("only treasure object can be added.")
            
    def get_treasure(self):
        ''' Returns all collected treasure. '''
        return self.__treasure
    
    def move(self, dx, dy):
        new_x = self.__x + dx
        new_y = self.__y + dy
        
        tile = map.get_tile(new_x, new_y)
        if tile is None:
            print("out of bounds.")
            return
        
        if self.can_move(tile) == False:
            print("This entity can't move to that tile.")
            return
        
    def can_move(self, tile):
        return False
    
class Pirate(GameEntity):
    def __init__(self, name, x=0, y=0, health=100):
        super().__init__(x, y, health)
        self.set_name(name)
        
    def set_name(self, name):
        if type(name) != str or len(name) == 0:
            print("name must not be empty. ")
        else:
            self.__name = name
    
    def get_name(self):
        return self.__name
    
    def can_move(self, tile):
        return type(tile).__name__ == "LandTile"
    
    
        
    
    
        
