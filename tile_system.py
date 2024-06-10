import pygame
from image_utils import load_coin_animation
from animation import coin_animation

"""==================================================================================================
The game is made up of tiles, this file stores the tile system, this controls where things are on the 
map and controls where the player can and cant move to.
====================================================================================================="""


class game_tiles:
    
    def __init__(self, tile_size: list[float], speed: float, file_path="None"):
        self.tile_size = tile_size

        # Map variable
        # -1 represents water, 0 is grass, -100 is the starting point, 100 is the end point of the game/maze
        # all other values represent different coin types and assets in the game

        self.map = [
            [-1, 4, 0,  4, -1, -1, -1, -1, -1, -1, -1, -1, 100, -1],
            [-1,  0, -1,  0, 0, 0, 2, -1,  0,  1,  0,  0,  4, -1],
            [-1,  5,  -1,  0, -1, -1, -1, -1,  0, -1, -1, -1,  0, -1],
            [-1, -1, -1,  4,  0,  1,  0, -1,  3, -1, -1,  2,  0, -1],
            [-1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1],
            [-1, -1, -1,  0, -1, -1,  3,  0, -1,  0,  0,  4, -1, -1],
            [-1,  2,  0,  4,  0,  1, -1,  4,  0,  1, -1,  0,  0,  3],
            [-1,  0, -1, -1, -1,  0, -1,  0, -1, -1, -1, -1,  0, -1],
            [-1,  0, -1, -1,  3,  0,  0,  2, -1, 5, 0,  4,  0, -1],
            [-1,  -100, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            ]
        
        self.speed = speed
        self.map_size = [10, 14]

        # Creates bindings for the player inputs and the direction which the player moves in for a given input
        
        self.control_to_offset = {
            pygame.K_UP: {"offset" :[-1,  0],"animation_name" : "walk_b"},
            pygame.K_LEFT: {"offset" :[0, -1], "animation_name" : "walk_l"},
            pygame.K_DOWN: {"offset" :[1, 0],  "animation_name" : "walk_f"},
            pygame.K_RIGHT: {"offset" :[0, 1],  "animation_name" : "walk_r"}
            }

        # Loading the textures used in the game
        self.grass = pygame.image.load("./assets/tiles/grass.png").convert_alpha()
        self.grass = pygame.transform.scale(self.grass, tile_size)
        
        self.water = pygame.image.load("./assets/tiles/water.png").convert_alpha()
        self.water = pygame.transform.scale(self.water, tile_size)
        
        self.treasure = pygame.image.load("./assets/tiles/finish.png").convert_alpha()
        self.treasure = pygame.transform.scale(self.treasure, (0.6*tile_size[0], 0.6*tile_size[0]))
        
        # Load the coins
        # Use sprite groups to easily handle the coins as a group and easily deal with collision detection
        self.coins1 = pygame.sprite.Group()
        self.coins2 = pygame.sprite.Group()
        self.coins3 = pygame.sprite.Group()
        self.coins4 = pygame.sprite.Group()
        self.coins5 = pygame.sprite.Group()
        
        # keep track of how many coins of each type are in the game
        # Used to compute the players score at any given moment
        # This is done by checking how many coins are in the group 
        # and comparing this to the total number of coins which were counted
        self.coin1_count = 0
        self.coin2_count = 0
        self.coin3_count = 0
        self.coin4_count = 0
        self.coin5_count = 0
        
        # Assign points to each coin type
        self.coin1_value = 15
        self.coin2_value = 10
        self.coin3_value = 5
        self.coin4_value = 1
        self.coin5_value = 50
        
        # Goes through the map variable and loads the required coins and assets
        y_index = 0
        for row in self.map:
            x_index = 0
            for col in row:
                if col == 1:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin3", "png", [0.65*tile_size[0], 0.65*tile_size[1]], 5), True, 8)
                    self.coins3.add(new_coin)
                    self.coin3_count += 1
                elif col == 2:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin2", "png", [0.65*tile_size[0], 0.65*tile_size[1]], 5), True, 8)
                    self.coins2.add(new_coin)
                    self.coin2_count += 1
                elif col == 3:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin1", "png", [0.65*tile_size[0], 0.65*tile_size[1]], 5), True, 8)
                    self.coins1.add(new_coin)
                    self.coin1_count += 1
                
                elif col == 4:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin4", "png", [0.65*tile_size[0], 0.65*tile_size[1]], 5), True, 8)
                    self.coins4.add(new_coin)
                    self.coin4_count += 1
                    
                elif col == 5:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/spr_coin_azu", "png", [0.65*tile_size[0], 0.65*tile_size[1]], 3), True, 4)
                    self.coins5.add(new_coin)
                    self.coin5_count += 1
                x_index += 1
                
            y_index += 1
        
        
    # Used to reset the game
    def load_coins(self):       
        # Load the coins
        self.coins1 = pygame.sprite.Group()
        self.coins2 = pygame.sprite.Group()
        self.coins3 = pygame.sprite.Group()
        self.coins4 = pygame.sprite.Group()
        self.coins5 = pygame.sprite.Group()
        
        self.coin1_count = 0
        self.coin2_count = 0
        self.coin3_count = 0
        self.coin4_count = 0
        self.coin5_count = 0
        
        self.coin1_value = 15
        self.coin2_value = 10
        self.coin3_value = 5
        self.coin4_value = 1
        self.coin5_value = 50
        
        y_index = 0
        for row in self.map:
            x_index = 0
            for col in row:
                if col == 1:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin3", "png", [0.65*self.tile_size[0], 0.65*self.tile_size[1]], 5), True, 8)
                    self.coins3.add(new_coin)
                    self.coin3_count += 1
                elif col == 2:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin2", "png", [0.65*self.tile_size[0], 0.65*self.tile_size[1]], 5), True, 8)
                    self.coins2.add(new_coin)
                    self.coin2_count += 1
                elif col == 3:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin1", "png", [0.65*self.tile_size[0], 0.65*self.tile_size[1]], 5), True, 8)
                    self.coins1.add(new_coin)
                    self.coin1_count += 1
                
                elif col == 4:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin4", "png", [0.65*self.tile_size[0], 0.65*self.tile_size[1]], 5), True, 8)
                    self.coins4.add(new_coin)
                    self.coin4_count += 1
                    
                elif col == 5:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/spr_coin_azu", "png", [0.65*self.tile_size[0], 0.65*self.tile_size[1]], 3), True, 4)
                    self.coins5.add(new_coin)
                    self.coin5_count += 1
                x_index += 1
                
            y_index += 1


    # COnverts an index on the map to a physical coordinate on the game
    def index_to_coord(self, index: list[int]):
        return [index[1] * self.tile_size[0] + (1/2)*self.tile_size[0], index[0] * self.tile_size[1] + (1/2)*self.tile_size[1]]
    
    # Draws the grass, water and coins onto the given screen variable
    def draw(self, screen: pygame.Surface):
        y_coord = 0
        for row in self.map:
            x_coord = 0
            for col in row:
                tile = pygame.rect.Rect(0, 0, self.tile_size[0], self.tile_size[1])
                tile.center = self.index_to_coord([y_coord, x_coord])
                if col != -1:
                    screen.blit(self.grass, tile)
                    if col == 100:
                        tile.centerx += 10
                        tile.centery += 5
                        screen.blit(self.treasure, tile)
                else:
                    screen.blit(self.water, tile)
                x_coord += 1
            y_coord += 1
        self.coins1.update()
        self.coins1.draw(screen)
        self.coins2.update()
        self.coins2.draw(screen)
        self.coins3.update()
        self.coins3.draw(screen)
        self.coins4.update()
        self.coins4.draw(screen)
        self.coins5.update()
        self.coins5.draw(screen)
                

    # Determines where the player goes given their current position and an input from the player
    def get_next_index(self, current_index: list[int], event: int):
        if self.control_to_offset.get(event):
            offset = self.control_to_offset.get(event)["offset"]
            animation_name = self.control_to_offset.get(event)["animation_name"]
            new_index = [current_index[0] + offset[0], current_index[1] + offset[1]]
            if self.is_index_valid(new_index):
                return [new_index, animation_name, self.offset_to_speed(offset)]
            else:
                return [None, animation_name, None]
        return [None, None, None]
            

    # Checks if a given index lies within the map variable
    # This prevents the player from going off the map and prevents the player from going into the water
    def is_index_valid(self, index: list[int]):
        if index[0] < 0 or index[0] > self.map_size[0] - 1 or index[1] < 0 or index[1] > self.map_size[1] - 1:
            return False
        return self.map[index[0]][index[1]] != -1
    

    def offset_to_speed(self, offset: list[int]):
        return [offset[0]*self.speed, offset[1]*self.speed]
    

    # Checks if the player has reached the treasure box
    def has_won(self, index: list[int]):
        if self.is_index_valid(index):
            if self.map[index[0]][index[1]] == 100:
                return True
            
        return False
    
    # Computes the score and gives it back to the game for futher processing
    def compute_score(self):
        return self.coin1_value*(self.coin1_count - len(self.coins1)) + self.coin2_value*(self.coin2_count - len(self.coins2)) + self.coin3_value*(self.coin3_count - len(self.coins3)) + self.coin4_value*(self.coin4_count - len(self.coins4)) + self.coin5_value*(self.coin5_count - len(self.coins5))