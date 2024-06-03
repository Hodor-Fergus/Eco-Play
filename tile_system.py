import pygame
from image_utils import load_coin_animation
from animation import coin_animation

class game_tiles:
    
    def __init__(self, tile_size: float, speed: float, file_path="None"):
        self.tile_size = tile_size
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
        
        self.control_to_offset = {
            pygame.K_w: {"offset" :[-1,  0],"animation_name" : "walk_b"},
            pygame.K_a: {"offset" :[0, -1], "animation_name" : "walk_l"},
            pygame.K_s: {"offset" :[1, 0],  "animation_name" : "walk_f"},
            pygame.K_d: {"offset" :[0, 1],  "animation_name" : "walk_r"}
            }

        self.grass = pygame.image.load("./assets/tiles/grass.png").convert_alpha()
        self.grass = pygame.transform.scale(self.grass, (tile_size, tile_size))
        
        self.water = pygame.image.load("./assets/tiles/water.png").convert_alpha()
        self.water = pygame.transform.scale(self.water, (tile_size, tile_size))
        
        self.treasure = pygame.image.load("./assets/tiles/finish.png").convert_alpha()
        self.treasure = pygame.transform.scale(self.treasure, (0.6*tile_size, 0.6*tile_size))
        
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
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin3", "png", [0.65*tile_size, 0.65*tile_size], 5), True, 8)
                    self.coins3.add(new_coin)
                    self.coin3_count += 1
                elif col == 2:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin2", "png", [0.65*tile_size, 0.65*tile_size], 5), True, 8)
                    self.coins2.add(new_coin)
                    self.coin2_count += 1
                elif col == 3:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin1", "png", [0.65*tile_size, 0.65*tile_size], 5), True, 8)
                    self.coins1.add(new_coin)
                    self.coin1_count += 1
                
                elif col == 4:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin4", "png", [0.65*tile_size, 0.65*tile_size], 5), True, 8)
                    self.coins4.add(new_coin)
                    self.coin4_count += 1
                    
                elif col == 5:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/spr_coin_azu", "png", [0.65*tile_size, 0.65*tile_size], 3), True, 4)
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
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin3", "png", [0.65*self.tile_size, 0.65*self.tile_size], 5), True, 8)
                    self.coins3.add(new_coin)
                    self.coin3_count += 1
                elif col == 2:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin2", "png", [0.65*self.tile_size, 0.65*self.tile_size], 5), True, 8)
                    self.coins2.add(new_coin)
                    self.coin2_count += 1
                elif col == 3:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin1", "png", [0.65*self.tile_size, 0.65*self.tile_size], 5), True, 8)
                    self.coins1.add(new_coin)
                    self.coin1_count += 1
                
                elif col == 4:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/coin4", "png", [0.65*self.tile_size, 0.65*self.tile_size], 5), True, 8)
                    self.coins4.add(new_coin)
                    self.coin4_count += 1
                    
                elif col == 5:
                    center = self.index_to_coord([y_index, x_index])
                    new_coin = coin_animation(center, load_coin_animation("./assets/coins/spr_coin_azu", "png", [0.65*self.tile_size, 0.65*self.tile_size], 3), True, 4)
                    self.coins5.add(new_coin)
                    self.coin5_count += 1
                x_index += 1
                
            y_index += 1


    def index_to_coord(self, index: list[int]):
        return [index[1] * self.tile_size + (1/2)*self.tile_size, index[0] * self.tile_size + (1/2)*self.tile_size]
    
    def draw(self, screen: pygame.Surface):
        y_coord = 0
        for row in self.map:
            x_coord = 0
            for col in row:
                tile = pygame.rect.Rect(0, 0, self.tile_size, self.tile_size)
                tile.center = self.index_to_coord([y_coord, x_coord])
                if col != -1:
                    screen.blit(self.grass, tile);
                    if col == 100:
                        tile.centerx += 10
                        tile.centery += 5
                        screen.blit(self.treasure, tile);
                else:
                    screen.blit(self.water, tile);
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
            

    def is_index_valid(self, index: list[int]):
        if index[0] < 0 or index[0] > self.map_size[0] - 1 or index[1] < 0 or index[1] > self.map_size[1] - 1:
            return False
        return self.map[index[0]][index[1]] != -1
    
    def offset_to_speed(self, offset: list[int]):
        return [offset[0]*self.speed, offset[1]*self.speed]
    
    def has_won(self, index: list[int]):
        if self.is_index_valid(index):
            if self.map[index[0]][index[1]] == 100:
                return True
            
        return False
    
    def compute_score(self):
        return self.coin1_value*(self.coin1_count - len(self.coins1)) + self.coin2_value*(self.coin2_count - len(self.coins2)) + self.coin3_value*(self.coin3_count - len(self.coins3)) + self.coin4_value*(self.coin4_count - len(self.coins4)) + self.coin5_value*(self.coin5_count - len(self.coins5))