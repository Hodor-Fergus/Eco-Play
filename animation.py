import pygame

class animation(pygame.sprite.Sprite):
    
    def __init__(self, coord: list[int], images: list[pygame.Surface], is_infinite: bool, animation_rate=1):
        pygame.sprite.Sprite.__init__(self)
        self.frames = images
        if self.frames == 0:
            print(f"WARNING: Animation created with no frames")
            return
        self.image = self.frames[0];
        self.rect = self.image.get_rect()
        self.rect.center = coord
        
        self.frame_index = 0
        self.animation_rate = animation_rate
        self.counter = 0
        self.is_infinite = is_infinite
        self.done = False
        
    def update(self):
        self.counter += 1
        if self.counter == self.animation_rate:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                if self.is_infinite:
                    self.frame_index = 0
                else:
                    self.done = True
                    
        if not self.done:
            self.image = self.frames[self.frame_index]
            
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        
    def reset(self):
        self.counter = 0
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.done = False
        
    

class coin_animation(animation):
    def __init__(self, coord: list[int], images: list[pygame.Surface], is_infinite: bool, animation_rate=1):
        animation.__init__(self, coord, images, is_infinite, animation_rate)
        self.coin_sound = pygame.mixer.Sound("./assets/sounds/coin.mp3")
        self.channel = pygame.mixer.Channel(2)
        
    def kill(self):
        self.channel.play(self.coin_sound)
        animation.kill(self)
        
                  
                