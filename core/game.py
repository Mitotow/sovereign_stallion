import pygame
from entities.player import Player
from core.constants import FPS, WINDOW_SIZE
from world.parallax import ParallaxSky
from world.collision import CollisionSystem
from world.map import MapSystem
from ui.landing.intro import IntroCinematic
from ui.landing.landing_menu import LandingMenu
from ui.main_menu import MainMenu
from ui.menu import Menu
from ui.ui_utils import blit_text
import core.constants as constants
from entities.base import Entity
from entities.enemy import Enemy


class Game():
    def __init__(self, debug_mode=False, fullscreen=False, skip=False):
        pygame.init()

        self.screen: pygame.Surface
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)

        # Debug
        self.debug_mode = debug_mode
        self.debug_entity: Entity | None = None
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.game_state = constants.INTRO if not skip else constants.MAIN_MENU
        self.game_difficulty = constants.DEFAULT_DIFFICULTY

        # UI
        self.font = None
        self.menus: dict[str, Menu] = {
            constants.INTRO: IntroCinematic(self.screen),
            constants.LANDING_MENU: LandingMenu(self.screen),
            constants.MAIN_MENU: MainMenu(self.screen),
        }
        self.menus[self.game_state].setup()

        # Game objects
        self.player: Player = None
        self.projectiles = pygame.sprite.Group()
        self.enemies: list[Enemy] = []
        
        # Managers
        self.collision_system: CollisionSystem = None
        self.map_system: MapSystem = None
        
        # World
        self.sky = None
        self.level_map = None
        self.map_image = None
        self.map_rect = None
        
    def setup_font(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)
            
    def create_enemies(self):
        enemy = Enemy(self.screen, pygame.Vector2(self.screen.get_rect().center))
        self.enemies.add(enemy)
        self.collision_system.add_dynamic(enemy)
        
    def setup(self):
        """
        Initialize game objects
        """
        self.setup_font()
        
        # Récupération de la difficulté dans le menu principal
        self.game_difficulty = self.menus[constants.MAIN_MENU].selected_difficulty

        # Joueur
        self.player = Player(self.screen, pygame.Vector2(100, 0))

        # Système de collision
        self.collision_system = CollisionSystem(self.screen)
        self.collision_system.add_dynamic(self.player)
            
        self.sky = ParallaxSky(self.screen)
        self.map_system = MapSystem(self.screen)
        self.collision_system.set_platforms(self.map_system.level_map.collision_rects)

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

        # DEBUG
        if self.debug_mode and pygame.mouse.get_pressed()[0]:
            self.debug_entity = self.collision_system.check_hover_dynamic(
                pygame.mouse.get_pos(),self.map_system.camera)

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
            enemy.update()
            
        for proj in self.projectiles:
            proj.update(self.dt)
            if not proj.alive():
                self.collision_system.remove(proj)
                
        self.map_system.camera.update(self.player)
            
    def handle_menu(self):
        """
        Récupère le menu actuel et change
        le game state en fonction de ce que
        renvoi le menu
        """
        
        current_menu: Menu | None = self.menus[self.game_state]
        if current_menu is None:
            return
        self.change_state(current_menu.update())
        
    def change_state(self, state: str):
        """
        Change l'état du jeu si celui-ci
        est différent. Setup et setdown
        les menus / setup le jeu.
        """
        
        if state != self.game_state:
            menu = self.menus.get(self.game_state)
            if menu:
                menu.setdown()
            self.game_state = state
            if state == constants.PLAYING:
                self.setup()
            else:
                menu = self.menus.get(self.game_state)
                if menu:
                    menu.setup()

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state in [constants.QUIT, constants.GAME_OVER]:
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
        
    def draw(self):
        if self.game_state in [constants.QUIT, constants.GAME_OVER]:
            return
        
        if self.game_state == constants.PLAYING:
            self.sky.draw(self.map_system.camera.camera.x)
            self.map_system.draw()
                
            for enemy in self.enemies:
                enemy.draw()

            for proj in self.projectiles:
                proj.draw()
                
            self.player.draw(self.map_system.camera)
            
            if self.debug_mode and self.font:
                self.show_debug()
        else:
            menu = self.menus[self.game_state]
            if menu:
                menu.draw()

    def show_debug(self):
        if self.debug_entity:
            self.debug_entity.show_debug(self.font, self.map_system.camera)

        for plat in self.map_system.level_map.collision_rects:
            pygame.draw.rect(self.screen, "red", self.map_system.camera.apply(plat.rect), 2)

        # Hitbox projectiles
        for proj in self.projectiles:
            pygame.draw.rect(self.screen, "yellow", proj.hb, 2)

        blit_text(self.screen,
                  f"fps={int(self.clock.get_fps())}, "
                  f"difficulty={self.game_difficulty}, "
                  f"dynamic_entities={len(self.collision_system.dynamic)}, "
                  f"platforms={len(self.collision_system.platforms)}",
                  (0, 0), self.font)
