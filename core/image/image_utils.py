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