from animation import animation
from image_utils import load_player_animation
import pygame

"""==============================================================
Created to represent the player
keeps track of the players animation and curretn position
also loads the required animations for the player

================================================================="""

class player(pygame.sprite.Sprite):
    
    def __init__(self, player_size: list[int], animation_rate: int, spawn_point: list[int]):
        # Define the paths for all the animations
        idle_f = "./assets/sprite_sheets/main_char/elf_front_idle/elf_front_idle"
        idle_l = "./assets/sprite_sheets/main_char/elf_side02_idle/elf_side02_idle"
        idle_r = "./assets/sprite_sheets/main_char/elf_side01_idle/elf_side01_idle"
        idle_b = "./assets/sprite_sheets/main_char/elf_back_idle/elf_back_idle"
        
        walk_f = "./assets/sprite_sheets/main_char/elf_front_walk/elf_front_walk"
        walk_l = "./assets/sprite_sheets/main_char/elf_side02_walk/elf_side02_walk"
        walk_r = "./assets/sprite_sheets/main_char/elf_side01_walk/elf_side01_walk"
        walk_b = "./assets/sprite_sheets/main_char/elf_back_walk/elf_back_walk"
        
        # Create a structure for all the animations
        self.animations = {
            "idle_f" : {"animation" : animation(spawn_point, load_player_animation(idle_f, 'png', player_size, 1), True, animation_rate),  "next" : None},
            "idle_l" : {"animation" : animation(spawn_point, load_player_animation(idle_l, 'png', player_size, 1), True, animation_rate),  "next" : None},
            "idle_r" : {"animation" : animation(spawn_point, load_player_animation(idle_r, 'png', player_size, 1), True, animation_rate),  "next" : None},
            "idle_b" : {"animation" : animation(spawn_point, load_player_animation(idle_b, 'png', player_size, 1), True, animation_rate),  "next" : None},
            "walk_f" : {"animation" : animation(spawn_point, load_player_animation(walk_f, 'png', player_size, 8), False, animation_rate), "next" : "idle_f"},
            "walk_l" : {"animation" : animation(spawn_point, load_player_animation(walk_l, 'png', player_size, 8), False, animation_rate), "next" : "idle_l"},
            "walk_r" : {"animation" : animation(spawn_point, load_player_animation(walk_r, 'png', player_size, 8), False, animation_rate), "next" : "idle_r"},
            "walk_b" : {"animation" : animation(spawn_point, load_player_animation(walk_b, 'png', player_size, 8), False, animation_rate), "next" : "idle_b"}
            }
        
        self.current_animation = self.animations["idle_b"]
        self.image = self.current_animation["animation"].image
        self.rect = self.image.get_rect()
        self.rect.center = spawn_point
        
        # Create key animation bindings
        self.key_animation_bindings = {
            pygame.K_LEFT : "walk_l",
            pygame.K_DOWN : "walk_f",
            pygame.K_UP : "walk_b",
            pygame.K_RIGHT : "walk_r"
            }
        
    def update(self):
        self.event_handler()
        self.current_animation["animation"].update()
        if self.current_animation["animation"].done:
            self.current_animation["animation"].reset()
            self.current_animation = self.animations[self.current_animation["next"]]
            self.current_animation["animation"].rect.center = self.rect.center

    # Selects the appropriate animation based on the given input from the user
    def event_handler(self):
        keys = pygame.key.get_pressed()
        for key in self.key_animation_bindings.keys():
            if keys[key]:
                self.current_animation = self.animations[self.key_animation_bindings[key]]
                self.current_animation["animation"].rect.center = self.rect.center
                
    # Draws the player onto the screen
    def draw(self, screen: pygame.Surface):
        self.current_animation["animation"].draw(screen)
        

    # Ensures that the players actual position and the players animation are in sync
    def update_animation_position(self, new_center: list[int]):
        self.current_animation["animation"].rect.center = new_center
