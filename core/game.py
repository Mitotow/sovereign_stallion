import pygame
from entities.player import Player
from core.constants import FPS, WINDOW_SIZE
from entities.enemy import Archer, Knight
from world.parallax import ParallaxSky
from core.collision import CollisionSystem
from core.map import MapSystem
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
        self.font_gameover = pygame.font.SysFont('Arial', 64, bold=True)

    def setup(self):
        self.setup_font()
        self.game_difficulty = self.menus[constants.MAIN_MENU].selected_difficulty

        # Joueur
        self.player = Player(self.screen, pygame.Vector2(100, 0))

        self.collision_system = CollisionSystem(self.screen)
        self.collision_system.add_dynamic(self.player)

        # Ennemis
        archer_test = Archer(self.screen, pygame.Vector2(900, 200))
        self.enemies.append(archer_test)
        self.collision_system.add_dynamic(archer_test)

        knight_test = Knight(self.screen, pygame.Vector2(1200, 200))
        self.enemies.append(knight_test)
        self.collision_system.add_dynamic(knight_test)

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
        
        if not self.player.is_alive:
            self.draw_world()
            # Affichage du message
            text_surface = self.font_gameover.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            self.screen.blit(text_surface, text_rect)
            return

        self.player.check_wall_sensors(self.map_system.level_map.collision_rects)
        self.player.update(self.dt)

        col_entity_plats = self.collision_system.update(self.dt)
        
        # Handle damage from platforms
        for collision in col_entity_plats:
            if collision[0] is self.player:
                # Récupération du tuple des platformes 
                # et récupérer la platforme de l'axe x
                platx = collision[1][0]
                if platx and platx.damage > 0:
                    self.player.take_damage(platx.damage)                   

        for enemy in self.enemies:
            enemy.update(self.dt, self)

        # DEBUG
        if self.debug_mode and pygame.mouse.get_pressed()[0]:
            self.debug_entity = self.collision_system.check_hover_dynamic(
                pygame.mouse.get_pos(), self.map_system.camera)

        # Collisions projectiles vs joueur
        hits = self.collision_system.check_group_overlap(self.projectiles, [self.player])
        for projectile, player in hits:
            if projectile.is_static: continue
            player.take_damage(10)
            projectile.kill()
            self.collision_system.remove(projectile)

        # Collisions ennemis vs joueur
        enemy_hits = self.collision_system.check_overlap(self.player, self.enemies)
        for enemy in enemy_hits:
            self.player.take_damage(10)

        # Projectiles
        for proj in self.projectiles:
            proj.update()
            if proj.hb.colliderect(self.player.hb):
                self.player.take_damage(10)
                proj.kill()
                self.collision_system.remove(proj)
                continue
            if not proj.alive():
                self.collision_system.remove(proj)

        # Mise à jour de la caméra
        self.map_system.camera.update(self.player)

    def handle_menu(self):
        current_menu: Menu | None = self.menus[self.game_state]
        if current_menu is None:
            return
        self.change_state(current_menu.update())

    def change_state(self, state: str):
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

    def draw_world(self):
        """ Déssine tous les éléments d'un niveau """
        cam = self.map_system.camera
        self.sky.draw(cam)
        self.map_system.draw()
        
        for enemy in self.enemies: enemy.draw(cam)
        for proj in self.projectiles: proj.draw(cam)
        self.player.draw(cam)
        
        self.draw_hearts()

    def draw(self):
        if self.game_state in [constants.QUIT, constants.GAME_OVER]:
            return
        
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
        cam = self.map_system.camera
        
        if self.debug_entity:
            self.debug_entity.show_debug(self.font, cam)

        for plat in self.map_system.level_map.collision_rects:
            pygame.draw.rect(self.screen, "red", cam.apply(plat.rect), 2)

        # Hitbox projectiles
        for proj in self.projectiles:
            pygame.draw.rect(self.screen, "yellow", cam.apply(proj.hb), 2)

        blit_text(self.screen,
                  f"fps={int(self.clock.get_fps())}, "
                  f"difficulty={self.game_difficulty}, "
                  f"dynamic_entities={len(self.collision_system.dynamic)}, "
                  f"platforms={len(self.collision_system.platforms)}",
                  (0, 0), self.font)

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
