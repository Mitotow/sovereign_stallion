import pygame

def get_image_chunks(path: str, lig = 1, col = 1, alpha = False):
    img = pygame.image.load(path)
    if alpha:
        img = img.convert_alpha()
    rect = img.get_rect()
    width, height = rect.width // col, rect.height // lig
    chunks: list[pygame.Surface] = []
    
    for i in range(lig):
        for j in range(col):
            chunks.append(img.subsurface(
                width * i, height * j, width, height))
    return chunks

def get_image_chunks_by_size(path: str, size: tuple[int, int], alpha = False):
    img = pygame.image.load(path)
    if alpha:
        img = img.convert_alpha()
    rect = img.get_rect()
    [width, height] = size
    lig, col = rect.width // width, rect.height // height
    chunks: list[pygame.Surface] = []
    
    for i in range(lig):
        for j in range(col):
            chunks.append(img.subsurface(
                width * i, height * j, width, height))
            
    return chunks