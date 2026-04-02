import pygame
from core.constants import SOLID
from core.assets.world_utils import get_world_assets
from world.platform import Platform

def read_tiled_map(path: str) -> list[list]:
    file = open("assets/world/maps/map01.csv")
    file.close()
    return [[]]

def load_map(path: str, screen: pygame.Surface) -> list[Platform]:
    map = read_tiled_map(path)
    platforms = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            code = map[i][j]
            if code < 0:
                continue
            get_world_assets(code)
            platform = Platform(screen, (0, 0), (32, 32), SOLID)
            platforms.append(platform)
    return platforms
        