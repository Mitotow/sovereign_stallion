import pygame
import os


class ParallaxSky:
    def __init__(self, screen: pygame.Surface):
        self.screen_width = screen.get_width()
        # 1. Dossier où se trouvent tes 5 images
        self.base_path = "world/ciel/"

        # 2. On définit les vitesses (plus le chiffre est petit, plus c'est loin)
        self.speeds = [0.05, 0.1, 0.2, 0.4, 0.6]

        # 3. Chargement des images (on suppose qu'elles se nomment layer_0.png à layer_4.png)
        self.layers = []
        for i in range(5):
            path = os.path.join(self.base_path, f"{i+1}.png")
            # On charge et on redimensionne à la taille de l'écran
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.screen_width, screen.get_height()))
            self.layers.append(img)

        self.screen_width

    def draw(self, screen, camera_x):
        for i, layer in enumerate(self.layers):
            # On calcule le décalage pour cette couche précise
            speed = self.speeds[i]
            # Le modulo (%) permet de faire boucler l'image à l'infini
            offset = (camera_x * speed) % self.screen_width

            # On dessine l'image deux fois pour combler le vide lors du défilement
            screen.blit(layer, (-offset, 0))
            screen.blit(layer, (self.screen_width - offset, 0))