import pygame
from entities.player import Player
from core.constants import FPS
from world.parallax import ParallaxSky
from world.collision import CollisionSystem
from world.platform import Platform
from ui.landing.intro import IntroCinematic
from ui.landing.landing_menu import LandingMenu
from ui.main_menu import MainMenu
from ui.menu import Menu
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
        self.menus: dict[str, Menu] = {
            constants.INTRO: IntroCinematic(self.screen),
            constants.LANDING_MENU: LandingMenu(self.screen),
            constants.MAIN_MENU: MainMenu(self.screen),
        }
        
        self.menus[self.game_state].setup()

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
        """
        Créer les platformes
        """
        
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
        
        # Récupération de la difficulté dans le menu principal
        self.game_difficulty = self.menus[constants.MAIN_MENU].selected_difficulty

        # Joueur
        self.player = Player(self.screen, pygame.Vector2(100, 0))
        self.sprites.add(self.player)

        # Système de collision
        self.collision_system = CollisionSystem(self.screen)
        self.collision_system.add_dynamic(self.player)

        self.create_platforms()
        self.sky = ParallaxSky(self.screen)

    def handle_playing(self):
        """
        Méthode principale de la gestion
        du jeu
        """
        
        self.screen.fill("black")

        if not self.player:
            return

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

        if self.debug_mode and self.font:
            self.show_debug()
            
    def handle_menu(self):
        """
        Récupère le menu actuel et change
        le game state en fonction de ce que
        renvoi le menu
        """
        
        current_menu: Menu | None = self.menus[self.game_state]
        if current_menu == None:
            return
        self.change_state(current_menu.update())
        
    def change_state(self, state: str):
        """
        Change l'état du jeu si celui-ci
        est différent. Setup et setdown
        les menus / setup le jeu.
        """
        
        if state != self.game_state:
            menu = self.menus[self.game_state]
            if menu:
                menu.setdown()
            self.game_state = state
            if state == constants.PLAYING:
                self.setup()
            else:
                menu = self.menus[self.game_state]
                if menu:
                    menu.setup()

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state == constants.QUIT:
                self.isRunning = False
            elif self.game_state == constants.PLAYING:
                self.handle_playing()
            else:
                self.handle_menu()

            self.draw()
            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()
        
    def draw(self):
        if self.game_state == constants.PLAYING:
            self.sky.draw(self.player.rect.x)
            
            self.player.draw()
            
            for plat in self.platforms:
                plat.draw()

            for enemy in self.enemies:
                enemy.draw()

            for proj in self.projectiles:
                proj.draw()
        else:
            menu = self.menus[self.game_state]
            if menu:
                menu.draw()

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
                  f"is_grounded={self.player.is_grounded}",
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
