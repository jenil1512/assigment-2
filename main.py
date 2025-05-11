class Treasure:
    def __init__(self, name, value):
        self.set_name(name)
        self.set_value(value)
        
    def set_name(self, name):
        ''' set treasure name and name cannot be empty.'''
        if type(name) == str and name !=" ":
            self.__name = name
        else:
            print("invalid name for treasure.")
    
    def get_name(self):
        ''' Return treasure name.'''
        return self.__name
    
    def set_value(self, value):
        ''' Set treasure value and it is must be in a positive integers.'''
        if type(value) == int and value > 0:
            self.__value = value
        else:
            print("Invalid value for treasure.")
            
    def get_value(self):
        ''' Returns treasure value.'''
        return self.__value
    
    def __str__(self):
        return f"{self.__name} ({self.__value} gold)"
    

class CannonBall:
    '''
    A class representing a cannonball used in a cannon to deal damage.
    '''
    def __init__(self, damage):
        self.set_damage(damage)

    def set_damage(self, damage):
        '''
        Sets the damage value. Must be a positive integer.
        '''
        if type(damage) == int and damage > 0:
            self.__damage = damage
        else:
            print("Error: damage must be a positive integer.")

    def get_damage(self):
        '''
        Returns the damage value of the cannonball.
        '''
        return self.__damage

    def __str__(self):
        return f"CannonBall (Damage: {self.__damage})"

    
class Cannon:
    def __init__(self):
        self._cannonball = 0

    def get_cannonball(self):
        return self._cannonball

    def set_cannonball(self, cannonball):
        if type(cannonball).__name__ == "CannonBall":
            self._cannonball = cannonball
        else:
            print("Only a CannonBall can be loaded.")

    def _fire(self):
        if self._cannonball:
            damage = self._cannonball.get_damage()
            self._cannonball = 0
            return damage
        else:
            print("Cannon is empty.")
            return 0

    def __str__(self):
        if self._cannonball:
            return f"Cannon loaded with {self._cannonball}"
        return "Cannon is empty"
  
        
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
        return " "
    
    def __repr__(self):
        return f"Tile(x={self.__x}, y = {self.__y}, object = {repr(self.__game_object)})"
        
class WaterTile(Tile):
    ''' Represents a water title. '''
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def display(self):
        ''' Returns a character based on the object on the water tile. '''
        obj = self.get_game_object()
        if obj != None:
            if type(obj).__name__ == "PirateShip":
                return "U" #player's ship
            elif type(obj).__name__ == "EnemyShip":
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
        if obj != None and type(obj).__name__ == "Pirate":
                if self.__treasure_container != None:
                    return "X" #pirate and treasure
                else:
                    return "o"
        return "+"
        

class Map:
    def __init__(self):
        self.__tiles = []
        self.__pirate = Pirate("jenil")
        self.__pirate_ship = Ship()        
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
            
        placed = False
        for row in self.__tiles:
            for tile in row:
                if type(tile).__name__ == "LandTile" and placed == False:
                    tile.set_game_object(self.__pirate)
                    placed = True
                    
        first_tile = self.get_tile(0,0)
        if type(first_tile).__name__ == "WaterTile":
            first_tile.set_game_object(self.__pirate_ship)
            
                 
    def get_tile(self,x,y):
        ''' Returns the tile at the given x and y coordinates. '''
        if y >= 0 and y < len(self.__tiles):
            if x >= 0 and x < len(self.__tiles[y]):
                return self.__tiles[y][x]
        return None
    
    def get_player(self):
        return self.__pirate
    
    def display_tiles(self):
        for row in self.__tiles:
            line = ""
            for tile in row:
                if tile != None:
                    line += tile.display() + " "
                else:
                    line += " "
            print(line.strip())

            
    def update_game_entities(self):
        for row in self.__tiles:
            for tile in row:
                entity = tile.get_game_object()
                
                if entity != 0:
                    if type(entity).__name__ == "EnemyShip":
                        entity.random_move() 
                        
class InvalidMoveException(Exception):
    ''' Rased when a game entity attempts to move to an invalid location.'''
    def __init__(self, message):
        super().__init__(message)
                        
class GameEntity:
    '''A parent class pirate and ship.'''
    def __init__(self, x=0, y=0, health=100):
        self.__x = x
        self.__y = y
        self.set_health(health)
        self.__treasure = []
        
    def move(self, dx, dy):
        ''' Move the entity by dx and dy. '''
        new_x = self.__x + dx
        new_y = self.__y + dy
        tile = map.get_tile(new_x, new_y)
        
        if tile == None:
            raise InvalidMoveException("Out of map bounds.")
        
        if self.can_move(tile) == False:
            raise InvalidMoveException("Cannot move to this tile.")
                        
        tile.set_game_object(self)
        self.__x = new_x
        self.__y = new_y     
        
    def can_move(self, tile):
        return False
          
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
    
    def get_treasure_value(self):
        total = 0
        for t in self.__treasure:
            total += t.get_value()
        return total 
    
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
    
    def dig(self):
        ''' pick up the treasure from the land tile if available. '''
        tile = map.get_tile(self.get_x(), self.get_y())
        if type(tile).__name__ != "LandTile":
            print("You can't dig on water.")
            return
        
        treasure = tile.get_treasure_container()
        if treasure == None:
            print("Nothing to dig here.")
            return
        
        self.add_treasure(treasure)
        tile.set_treasure_container(None)
        print("You found treasure!")
        
class Ship(GameEntity):
    def __init__(self, x=0, y=0, health=100):
        super().__init__(x, y, health)
        self.__cannon = Cannon()
        
    def reload_cannon(self, damage):
        cannonball = CannonBall(damage)
        self.__cannon.set_cannonball(cannonball)
        print("Cannon reloaded.")
        
    def fire_cannon(self):
        damage = self.__cannon._fire()
        print(f"Ship fired. Damage: {damage}")
        return damage

    def can_move_to(self, tile):
        return type(tile).__name__ == "WaterTile"
    
class EnemyShip(Ship):
    def __init__(self, x=0, y=0, health=100):
        super().__init__(x, y, health)
        
    def random_move(self):
        import random
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy)          
            
    
def main():
        
        map = Map()
        choice = None
        
        while choice != "quit":
            try:
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
            except InvalidMoveException as e:
                print(e)
                
            map.display_tiles()
            choice = input("Enter w, a, s, d, dig, or quit: ")
            map.update_game_entities()
        
        print("Goodbye")
        
if __name__ == "__main__":
    main()
        
        
    
        
    
    
        
