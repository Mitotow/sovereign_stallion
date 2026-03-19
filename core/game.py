import pygame
from entities.player import Player
from core.constants import FPS
from world.parallax import ParallaxSky
from world.collision import CollisionSystem
from world.platform import Platform
from ui.landing.intro import IntroCinematic
from ui.landing.landing_menu import LandingMenu
from ui.main_menu import MainMenu
from ui.ui_utils import blit_text
import core.constants as constants


class Game():
    def __init__(self, window_size, debug_mode=False, fullscreen=False):
        pygame.init()

        self.screen: pygame.Surface
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
        self.sprites = pygame.sprite.Group()

        # UI
        self.intro = IntroCinematic(self.screen)
        self.landing_menu = LandingMenu(self.screen)
        self.main_menu = MainMenu(self.screen)

        # Start intro cinematic
        self.intro.start()

        # Game objects
        self.player = None
        self.platforms = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collision_system = None
        self.sky = None
        self.font = None

    def setup_font(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)

    def create_platforms(self):
        w = self.screen.get_width()
        h = self.screen.get_height()

        platforms = [
            Platform(self.screen, pygame.Vector2(0, h), (w, 20), "solide"),
            Platform(self.screen, pygame.Vector2(200, h - 150), (200, 20), "solide"),
            Platform(self.screen, pygame.Vector2(500, h - 300), (200, 20), "solide"),
            Platform(self.screen, pygame.Vector2(100, h - 450), (150, 20), "traversable"),
        ]
        for p in platforms:
            self.collision_system.add_platform(p)
            self.platforms.add(p)

    def setup(self):
        """
        Initialize game objects
        """
        self.setup_font()

        # Joueur
        self.player = Player(self.screen, pygame.Vector2(100, 0))
        self.sprites.add(self.player)

        # Système de collision
        self.collision_system = CollisionSystem(self.screen)
        self.collision_system.add_dynamic(self.player)

        self.create_platforms()
        self.sky = ParallaxSky(self.screen)

    def handle_playing(self):
        self.screen.fill("black")

        if not self.player:
            return

        self.sky.draw(self.player.rect.x)
        self.player.update(self.dt)
        self.collision_system.update(self.dt)

        # Collisions projectiles vs joueur
        hits = self.collision_system.check_group_overlap(self.projectiles, [self.player])
        for projectile, player in hits:
            player.take_damage(10)
            projectile.kill()
            self.collision_system.remove(projectile)

        # Collisions ennemis vs joueur
        enemy_hits = self.collision_system.check_overlap(self.player, self.enemies)
        for enemy in enemy_hits:
            self.player.take_damage(10)

        for enemy in self.enemies:
            enemy.update(self.dt)
            
        for proj in self.projectiles:
            proj.update(self.dt)
            if not proj.alive():
                self.collision_system.remove(proj)

        self.draw()

        if self.debug_mode and self.font:
            self.show_debug()

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state == constants.INTRO:
                # Handle intro
                if self.intro.update() == constants.INTRO_FINISHED:
                    self.game_state = constants.LANDING_MENU
                    self.landing_menu.start_music()
                self.intro.draw()

            elif self.game_state == constants.LANDING_MENU:
                # Handle landing menu
                if self.landing_menu.update() == constants.MAIN_MENU:
                    pygame.mixer.music.fadeout(1000)
                    self.game_state = constants.MAIN_MENU
                self.landing_menu.draw()

            elif self.game_state == constants.MAIN_MENU:
                # Handle main menu
                self.main_menu.draw(self.screen)
                choice = self.main_menu.check_click()
                if choice == constants.PLAYING:
                    self.game_difficulty = self.main_menu.selected_difficulty
                    self.setup()
                self.game_state = choice

            elif self.game_state == constants.PLAYING:
                self.handle_playing()

            elif self.game_state == constants.GAME_OVER:
                # TODO: écran game over
                pass

            elif self.game_state == constants.QUIT:
                self.isRunning = False

            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()
        
    def draw(self):
        self.player.draw()

        for plat in self.platforms:
            plat.draw()

        for enemy in self.enemies:
            enemy.draw()

        for proj in self.projectiles:
            proj.draw()

    def show_debug(self):
        # Hitbox / Rect du joueur
        pygame.draw.rect(self.screen, "red", self.player.hb, 2)
        pygame.draw.rect(self.screen, "green", self.player.rect, 1)

        # Hitbox platformes
        for plat in self.platforms:
            color = "red" if plat.type == "solide" else "blue"
            pygame.draw.rect(self.screen, color, plat.rect, 2)

        # Hitbox ennemis
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, "orange", enemy.hb, 2)

        # Hitbox projectiles
        for proj in self.projectiles:
            pygame.draw.rect(self.screen, "yellow", proj.hb, 2)

        # Information du jeu
        blit_text(self.screen,
                  f"pos_x={self.player.rect.x}, pos_y={self.player.rect.y}, "
                  f"hb_x={self.player.hb.x}, hb_y={self.player.hb.y}",
                  (0, 0), self.font)
        blit_text(self.screen,
                  f"vel_x={self.player.velocity.x:.2f}, vel_y={self.player.velocity.y:.2f}, "
                  f"is_grounded={self.player.is_grounded}, is_falling={self.player.is_falling}",
                  (0, 20), self.font)
        blit_text(self.screen,
                  f"current_state={self.player.current_state}, "
                  f"spritesheet_len={len(self.player.current_animation.frames)}",
                  (0, 40), self.font)
        blit_text(self.screen,
                  f"difficulty={self.game_difficulty}, "
                  f"dynamic_entities={len(self.collision_system.dynamic)}, "
                  f"platforms={len(self.collision_system.platforms)}",
                  (0, 60), self.font)
