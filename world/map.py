import pygame
import pytmx

class ssmap:
    def __init__(self, filename):
        # Charge le fichier .tmx
        self.tmxdata = pytmx.util_pygame.load_pygame(filename)
        # Calcule les dimensions totales de la carte en pixels
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        # Parcourt tous les calques (layers) créés dans Tiled
        for layer in self.tmxdata.visible_layers:
            # On ne dessine que les calques de tuiles (on ignore les objets pour l'instant)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        # Dessine la tuile à sa position exacte
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        # Crée une surface vide transparente de la taille du niveau complet
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface