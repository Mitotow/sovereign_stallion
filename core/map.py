import pygame
import pytmx
import core.constants as constants
from core.camera import Camera
from world.platform import Platform

class ssmap:
    def __init__(self, filename):
        self.tmxdata = pytmx.util_pygame.load_pygame(filename)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.collision_rects = self._load_collisions()

    def _load_collisions(self):
        platforms = []
        layer = self.tmxdata.get_layer_by_name(constants.GROUND_LAYER)
        for obj in layer:
            plat = Platform(int(obj.x), int(obj.y), int(obj.width), int(obj.height))
            platforms.append(plat)

        layer = self.tmxdata.get_layer_by_name(constants.LAVA_LAYER)
        for obj in layer:
            plat = Platform(int(obj.x), int(obj.y), int(obj.width), int(obj.height), platform_type=constants.TAVERSABLE, damage=30)
            platforms.append(plat)

        return platforms

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (
                            x * self.tmxdata.tilewidth,
                            y * self.tmxdata.tileheight
                        ))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface


class MapSystem:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.level_id = 0
        self.level_map: ssmap = None
        self.map_image: pygame.Surface = None
        self.map_rect: pygame.Rect = None
        self.camera: Camera = None
        self.maps = []
        
        for map in constants.MAPS:
            self.maps.append(ssmap(constants.MAPS_BASEURL.format(map)))
            
        self.load_level(self.level_id)
    
    def load_level(self, id: int):
        if id < 0 or id >= len(self.maps):
            return
        
        self.level_map = self.maps[id]
        self.map_image = self.level_map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.map_rect.bottom = self.screen.get_height() + constants.MAPS_OFFSET_Y
        self.camera = Camera(self.screen, self.level_map.width, self.level_map.height + self.map_rect.y)
        
        # Décallage des plateformes sur y
        map_offset_y = self.map_rect.y
        for plat in self.level_map.collision_rects:
            plat.rect.y += map_offset_y
        
        self.level_id = id
        
    def draw(self):
        self.screen.blit(self.map_image, self.camera.apply(self.map_rect))
