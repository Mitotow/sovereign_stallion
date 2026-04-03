import pygame
from entities.player import Player
from core.constants import FPS
from world.parallax import ParallaxSky
from ui.landing.intro import IntroCinematic
from ui.landing.landing_menu import LandingMenu
from ui.main_menu import MainMenu
from ui.ui_utils import blit_text
import core.constants as constants
from world.map import ssmap
from core.camera import Camera


class Game():
    def __init__(self, window_size, debug_mode=False, fullscreen=False):
        pygame.init()

        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(window_size)
        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.game_state = constants.INTRO
        self.game_difficulty = constants.DEFAULT_DIFFICULTY

        # UI
        self.intro = IntroCinematic(self.screen)
        self.landing_menu = LandingMenu(self.screen)
        self.main_menu = MainMenu(self.screen)

        # Start intro cinematic
        self.intro.start()

        self.player = None
        self.camera = None
        self.sky = None
        self.level_map = None
        self.map_image = None
        self.map_rect = None
        self.font = None

    def setup_font(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)



    def setup(self):
            self.setup_font()

            # 1. Initialisation du joueur et du ciel
            self.player = Player(pygame.Vector2(100, 100))
            self.sky = ParallaxSky(self.screen)

            # 2. Chargement de la carte (vérifie bien le nom du fichier ssmapping.tmx)
            self.level_map = ssmap('assets/map/ssmapping2.tmx')
            self.map_image = self.level_map.make_map()

            # 3. Calcul du positionnement (très important pour l'affichage)
            self.map_rect = self.map_image.get_rect()
            # On cale le bas de la map sur le bas de l'écran
            self.map_rect.bottom = self.screen.get_height() + 310

            self.camera = Camera(self.level_map.width, self.level_map.height,
                         self.screen.get_width(), self.screen.get_height())

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state == constants.INTRO:
                if self.intro.update() == constants.INTRO_FINISHED:
                    self.game_state = constants.LANDING_MENU
                    self.landing_menu.start_music()
                self.intro.draw()

            elif self.game_state == constants.LANDING_MENU:
                if self.landing_menu.update() == constants.MAIN_MENU:
                    pygame.mixer.music.fadeout(1000)
                    self.game_state = constants.MAIN_MENU
                self.landing_menu.draw()

            elif self.game_state == constants.MAIN_MENU:
                self.main_menu.draw(self.screen)
                choice = self.main_menu.check_click()
                if choice == constants.PLAYING:
                    self.game_difficulty = self.main_menu.selected_difficulty
                    self.setup()
                self.game_state = choice



            elif self.game_state == constants.PLAYING:

                self.screen.fill("black")

                if self.player and self.sky and self.map_image and self.camera:

                    # 1. Mise à jour de la caméra (elle suit le joueur)

                    self.camera.update(self.player)

                    # 2. Dessiner le ciel (Parallaxe)

                    # On passe le décalage x de la caméra au ciel pour qu'il bouge aussi

                    self.sky.draw(self.screen, self.camera.camera.x)

                    # 3. Dessiner la MAP avec le décalage caméra

                    self.screen.blit(self.map_image, self.camera.apply(self.map_rect))

                    # 4. Physique du joueur

                    self.player.run(self.dt, self.screen)

                    # 5. Dessiner le joueur avec le décalage caméra

                    self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

                    if self.debug_mode and self.font:
                        self.show_debug()

            elif self.game_state == constants.QUIT:
                self.isRunning = False

            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()

    def show_debug(self):
        # On dessine la hitbox du joueur
        pygame.draw.rect(self.screen, "red", self.player.hb, 2)
        blit_text(self.screen, f"pos_x={self.player.rect.x:.0f}, pos_y={self.player.rect.y:.0f}", (10, 10), self.font)
        blit_text(self.screen, f"vel_x={self.player.velocity.x:.2f}, vel_y={self.player.velocity.y:.2f}", (10, 30),
                  self.font)
        blit_text(self.screen, f"state={self.player.current_state}", (10, 50), self.font)