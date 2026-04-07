import pygame
from entities.player import Player
from entities.enemy import Archer, Knight
from core.constants import FPS, WINDOW_SIZE, SOLID, TAVERSABLE
from core.map import load_map
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
    def __init__(self, debug_mode=False, fullscreen=False, skip=False):
        pygame.init()

        self.screen: pygame.Surface
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.game_state = constants.INTRO if not skip else constants.MAIN_MENU
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
        self.font_gameover = pygame.font.SysFont('Arial', 64, bold=True)

    def create_platforms(self):
        w = self.screen.get_width()
        h = self.screen.get_height()

        platforms = [
            Platform(self.screen, pygame.Vector2(0, h), (w, 20), SOLID),
            Platform(self.screen, pygame.Vector2(200, h - 150), (200, 20), SOLID),
            Platform(self.screen, pygame.Vector2(500, h - 300), (200, 20), SOLID),
            Platform(self.screen, pygame.Vector2(100, h - 450), (150, 20), TAVERSABLE),
        ]

        for p in platforms:
            self.collision_system.add_platform(p)
            self.platforms.add(p)

    def setup(self):
        self.setup_font()
        self.game_difficulty = self.menus[constants.MAIN_MENU].selected_difficulty

        # Joueur
        self.player = Player(self.screen, pygame.Vector2(100, 0))
        self.sprites.add(self.player)

        self.collision_system = CollisionSystem(self.screen)
        self.collision_system.add_dynamic(self.player)

        # Ennemis
        archer_test = Archer(self.screen, pygame.Vector2(900, 200))
        self.enemies.add(archer_test)
        self.collision_system.add_dynamic(archer_test)

        knight_test = Knight(self.screen, pygame.Vector2(1200, 200))
        self.enemies.add(knight_test)
        self.collision_system.add_dynamic(knight_test)

        self.create_platforms()
        self.sky = ParallaxSky(self.screen)

    def handle_playing(self):
        self.screen.fill("black")

        if not self.player:
            return
        if not self.player.is_alive:
            self.draw_world()
            # Affichage du message
            text_surface = self.font_gameover.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
            self.screen.blit(text_surface, text_rect)
            return

        self.player.update(self.dt)
        self.collision_system.update(self.dt)

        # 1. Projectiles
        for proj in self.projectiles.copy():
            proj.update(self.dt)
            if proj.hb.colliderect(self.player.hb):
                self.player.take_damage(10)
                proj.kill()
                self.collision_system.remove(proj)
                continue
            if not proj.alive():
                self.collision_system.remove(proj)

        # 2. Collisions ennemis
        enemy_hits = self.collision_system.check_overlap(self.player, self.enemies)
        for enemy in enemy_hits:
            if isinstance(enemy, Knight):
                self.player.take_damage(30)
            else:
                self.player.take_damage(5 * self.dt)

        # 3. IAs
        for enemy in self.enemies:
            enemy.update(self.dt, self)

    def handle_menu(self):
        current_menu: Menu | None = self.menus[self.game_state]
        if current_menu == None:
            return
        self.change_state(current_menu.update())

    def change_state(self, state: str):
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
                break
            elif self.game_state == constants.PLAYING:
                self.handle_playing()
            else:
                self.handle_menu()

            self.draw()
            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()

    def draw_world(self):
        """Regroupe tout le dessin du niveau pour la réutilisation"""
        self.sky.draw(self.player.rect.x)
        self.player.draw()
        for plat in self.platforms: plat.draw()
        for enemy in self.enemies: enemy.draw()
        for proj in self.projectiles: proj.draw()
        self.draw_hearts()

    def draw(self):
        if self.game_state == constants.PLAYING:
            if self.player and self.player.is_alive:
                self.draw_world()

            if self.debug_mode and self.font:
                self.show_debug()
        else:
            menu = self.menus[self.game_state]
            if menu:
                menu.draw()

    def show_debug(self):
        pygame.draw.rect(self.screen, "red", self.player.hb, 2)
        for plat in self.platforms:
            color = "red" if plat.type == SOLID else "blue"
            pygame.draw.rect(self.screen, color, plat.rect, 2)
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, "orange", enemy.hb, 2)
        for proj in self.projectiles:
            pygame.draw.rect(self.screen, "yellow", proj.hb, 2)

    def draw_hearts(self):
        """Affiche des coeurs en haut à gauche"""
        for i in range(3):
            x = 40 + (i * 45)
            y = 35
            color = (255, 0, 0) if self.player.hp > (i * 10) else (60, 60, 60)
            points = [
                (x, y + 15), (x - 15, y - 5), (x - 8, y - 12),
                (x, y - 5), (x + 8, y - 12), (x + 15, y - 5)
            ]
            pygame.draw.polygon(self.screen, color, points)