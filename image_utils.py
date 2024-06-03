import pygame

"""============================================================================================
Some functions to help load player animations (sprites) onto the game
==============================================================================================="""

def load_player_animation(base_path: str, file_extension: str, image_size: list[int], frame_count: int):
    images = []
    
    if frame_count == 1:
        image = pygame.image.load(f"{base_path}.{file_extension}").convert_alpha()
        image = pygame.transform.scale(image, image_size)
        images.append(image)
    
    else:
        for i in range(1, frame_count + 1):
            image = pygame.image.load(f"{base_path}{i}.{file_extension}").convert_alpha()
            image = pygame.transform.scale(image, image_size)
            images.append(image)
    return images


def load_coin_animation(base_path: str, file_extension: str, image_size: list[int], frame_count: int):
    images = []
    
    sheet = pygame.image.load(f"{base_path}.{file_extension}").convert_alpha()
    for i in range(frame_count):
        image = pygame.surface.Surface((16, 16), pygame.SRCALPHA)
        sub_image = pygame.rect.Rect(i * 16, 0, 16, 16)
        image.blit(sheet, image.get_rect(), sub_image)
        image = pygame.transform.scale(image, image_size)
        images.append(image)
    return images