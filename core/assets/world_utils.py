import pygame
from core.assets.utils import get_image_chunks_by_size
import core.constants as constants

cached_world_assets: dict[int, list[list[pygame.Surface]]] = {}

def get_world_assets_info(code: int) -> tuple[int, int]:
    id = code // 100
    return (id, code - id*100)

def load_world_assets(id: int) -> list[list[pygame.Surface]]:
    path = constants.WORLD_ASSETS_BASE.format(id)
    chunks = get_image_chunks_by_size(path, constants.TILE_SIZE, alpha=True)
    cached_world_assets[id] = chunks
    
    return chunks

def get_world_assets(code: int) -> pygame.Surface:
    [id, index] = get_world_assets_info(code)
    data = cached_world_assets.get(id)
    if not data:
        data = load_world_assets(id)
    
    return data[index]
    